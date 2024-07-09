#!/usr/bin/env python3
"""
Lists all unique timestamps in a directory of recordings
lets you use the pick module to select a timestamp, that
then open videos including that timestamp in mpv side
by side.
"""

__author__ = "Mikkel Rask"
__version__ = "0.2.0"
__license__ = "MIT"

import pick
import os
import re
from datetime import datetime
from collections import OrderedDict
from pathlib import Path
from typing import List, Dict

directory = Path("/pool/skadecam")
file_types = [".mp4"]


def get_files(directory: Path) -> List[str]:
    """get all files in the listed directory"""
    if not directory.exists() or not directory.is_dir():
        raise FileNotFoundError(
            f"Directory {directory} does not exist or is not a directory"
        )
    return [str(file) for file in directory.iterdir() if file.suffix in file_types]


def clean_files(files: List[str]) -> List[str]:
    """remove -TOP_VIEW, TOP-VIEW-, -BOTTOM_VIEW, BOTTOM_VIEW- and .mp4 from the file names"""
    pattern = re.compile(r"(-?TOP_VIEW-?)|(-?BOTTOM_VIEW-?)|(\.mp4)")
    return [pattern.sub("", Path(file).stem) for file in files if len(file) > 4]


def format_timestamps(files: List[str]) -> List[str]:
    """formats the timestamps to a more readable format"""
    formatted = []
    for file in files:
        date_part, time_part = file.split("-")
        formatted_date = f"{date_part[:2]}/{date_part[2:4]}/{date_part[4:]}"
        formatted_time = f"{time_part[:2]}:{time_part[2:4]}:{time_part[4:]}"
        formatted.append(f"{formatted_date} {formatted_time}")
    return formatted


def create_mapping(
    original_files: List[str], formatted_files: List[str]
) -> Dict[str, str]:
    """creates a mapping from formatted timestamps to original files"""
    return dict(zip(formatted_files, original_files))


def sort_files(files: List[str]) -> List[str]:
    """makes sure the timestamps are sorted"""
    return sorted(files, key=lambda x: datetime.strptime(x, "%d%m%Y-%H%M%S"))


def remove_duplicates(files: List[str]) -> List[str]:
    """removes duplicates, to unclutter the list"""
    return list(OrderedDict.fromkeys(files))


def play_selected(
    allFiles: List[str], original_files: Dict[str, str], selected: str
) -> None:
    """play the files corresponding to the selected timestamp"""
    for file in allFiles:
        if original_files[selected] in file:
            if "TOP_VIEW" in file:
                os.system(f"mpv {directory / file} --video-rotate=270 &")
            else:
                os.system(f"mpv {directory / file} &")


def main():
    """List all the unique timestamp/recordings"""
    title = "  PLEASE SELECT A RECORDING TO PLAY::"
    allFiles = get_files(directory)
    cleaned_files = clean_files(allFiles)
    sorted_files = sort_files(cleaned_files)
    unique_sorted_files = remove_duplicates(sorted_files)
    pretty_files = format_timestamps(unique_sorted_files)
    file_mapping = create_mapping(unique_sorted_files, pretty_files)
    option, _ = pick.pick(pretty_files, title)
    play_selected(allFiles, file_mapping, option)


if __name__ == "__main__":
    """ Run the main function """
    main()
