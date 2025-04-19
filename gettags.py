#!/usr/bin/python3
import os
import sys
import argparse
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.oggvorbis import OggVorbis
from mutagen.aac import AAC
from mutagen.mp4 import MP4
from mutagen.id3 import ID3

def get_id3_tags(filename):
    """
    Retrieves ID3 tags from a music file.
    Args:
        filename: The path to the music file.
    Returns:
        A dictionary containing the ID3 tags.  Returns None if the file doesn't
        have ID3 tags, or if an error occurs.
    """
    try:
        if filename.endswith(".mp3"):
            audio = MP3(filename)
        elif filename.endswith(".flac"):
            audio = FLAC(filename)
        elif filename.endswith(".ogg"):
            audio = OggVorbis(filename)
        elif filename.endswith((".aac", ".m4a", ".m4b")):
            audio = MP4(filename)
        else:
            print(f"Unsupported file format: {filename}")
            return None
        return audio.tags
    except Exception as e:
        print(f"Error: Could not read EasyID3 tags from {filename}.  File may not be a standard ID3 file: {e}")
        return None
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return None

def getAlbum(filename):
    """
    Retrieves ID3 tags from a music file.
    Args:
        filename: The path to the music file.
    Returns:
        A dictionary containing the ID3 tags.  Returns None if the file doesn't
        have ID3 tags, or if an error occurs.
    """
    try:
        if filename.endswith(".mp3"):
            audio = MP3(filename)
            return str(audio["TALB"])
        elif filename.endswith(".flac"):
            audio = FLAC(filename)
        elif filename.endswith(".ogg"):
            audio = OggVorbis(filename)
        elif filename.endswith((".aac", ".m4a", ".m4b")):
            audio = MP4(filename)
            return str(audio["©alb"][0])
        else:
            print(f"Unsupported file format: {filename}")
            return None
        return audio.tags
    except Exception as e:
        print(f"Error: Could not read EasyID3 tags from {filename}.  File may not be a standard ID3 file: {e}")
        return None
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return None


def main():
    """
    Parses command-line arguments and prints ID3 tags for the given files.
    """
    parser = argparse.ArgumentParser(description="Prints ID3 tags from music files.")
    parser.add_argument("files", nargs='+', help="The names of the music files to process.")
    args = parser.parse_args()

    for filename in args.files:
        album=getAlbum(filename)
        album=album.replace(":", ";")
        album=album.replace("/", "_")
        album=album.replace("\\", "_")
        os.makedirs(album, exist_ok=True)
        os.rename(filename, f"{album}/{filename}")
        print(f"Moved '{filename}' to '{album}/{filename}'")
    sys.exit(0)

    for filename in args.files:
        tags = get_id3_tags(filename)
        if tags:
            print(f"ID3 Tags for {filename}:")
            for key, value in tags.items():
                if not key in ("covr", "APIC:"):
                    print(f"  {key}: {value}")
            print("-" * 20)


if __name__ == "__main__":
    main()
