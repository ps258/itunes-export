#!/usr/bin/python3
from libpytunes import Library
from libpytunes import Playlist
from pathlib import Path
import os
import argparse

parser = argparse.ArgumentParser(description="An utility application to export iTunes playlists in m3u format.")
parser.add_argument("--output", "-o", help="The outpout folder for exporting the playlists.", required=True)
parser.add_argument("--ignore", help="Ignore a specific playlist.", action='append')
parser.add_argument("--library", "-l", help="The path to the iTunes Library XML.", default=str(Path.home().joinpath("Music/iTunes/iTunes Music Library.xml")))
parser.add_argument("--relative", "-r", action='store_true', help="Use paths relative to the iTunes library in the playlists")
parser.add_argument("--export-genius-playlists", action='store_true', dest='exportGeniusPlaylists')
parser.add_argument("--export-smart-playlists", action='store_true', dest='exportSmartPlaylists')
args = parser.parse_args()

libraryPath = args.library
playlistRootPath = Path(args.output)
ignoreList= args.ignore if args.ignore is not None else []

def cleanupPlaylistName(playlistName):
        return playlistName.replace("/", "").replace("\\", "").replace(":", "")

def exportPlaylist(playlist: Playlist, parentPath: Path):
    if(playlist.is_genius_playlist and not args.exportGeniusPlaylists):
        return

    if(playlist.is_smart_playlist and not args.exportSmartPlaylists):
        return

    if(playlist.is_folder):
        # Create Folder
        currentPath = parentPath.joinpath(playlist.name)
        if(not currentPath.exists()):
            currentPath.mkdir()

        for childPlaylist in list(playlists.values()):
            if(childPlaylist.parent_persistent_id == playlist.playlist_persistent_id):
                exportPlaylist(childPlaylist, currentPath)
    else:
        playlistContent = ""
        # cmus ignores the metadata tags so we skip them and get around renaming the playlist using script that calls cmus-remote
        #playlistContent = f"#EXTM3U\n#PLAYLIST:{playlist.name}\n"
        for track in playlist.tracks:
            if args.relative:
                if track.location != None:
                    try:
                        playlistContent +=  os.path.relpath(track.location, start=parentPath) + "\n"
                    except ValueError:
                        print(("Warning: Could not add the track \"" + track.location + "\" as relative path to the playlist \"" + playlistName + "\"; added the track as absolute path instead."))
                        playlistContent += track.location + "\n"
            else:
                playlistContent += "/" + track.location + "\n"

            playlistPath = parentPath.joinpath(cleanupPlaylistName(playlist.name) + ".m3u")
            playlistPath.write_text(playlistContent, encoding="utf8")

playlists = {}

library = Library(libraryPath)
for playlistName in library.getPlaylistNames(ignoreList=[
        "Library", "Music", "Movies", "TV Shows", "Purchased", "iTunes DJ", "Podcasts", "Audiobooks", "Downloaded"
] + ignoreList):
    playlist = library.getPlaylist(playlistName)
    playlists[playlist.playlist_persistent_id] = playlist

for playlist in list(playlists.values()): 
    if(playlist.parent_persistent_id == None) :
        exportPlaylist(playlist, playlistRootPath)
