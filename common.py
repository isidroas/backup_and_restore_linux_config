import os
import shutil
from typing import Tuple
from pathlib import Path

import difflib
from datetime import datetime
from colorama import Fore, Style
import click
from datetime import datetime

EXCLUDE_FOLDER = [".git", ".mypy_cache"]
EXCLUDE_FILE = ["TODO.md", ".swp"]


def get_user_path(path: str) -> str:
    list_ = path.split("/")

    if list_[1] != "home":
        raise ValueError(f"path: {path} is not an absolute path")

    return list_[2]


def change_user_path(path: Path, new_user: str) -> Path:
    """ Change user name of the path. The given path shoud be absolute and
    therefore the user name is in the second position (after 'home' folder)

    >>> change_user_of_path(Path('/home/foo/.local/bin/myprogram.sh'), 'bar')
    Path('/home/bar/.local/bin/myprogram.sh')
    """
    if not path.is_absolute():
        raise ValueError("Path is not absolute")

    if len(path.parts)>2 and path.parts[1] != "home":
        return path

    parts = list(path.parts)
    #import pdb; pdb.set_trace()
    parts[2] = new_user
    path = Path(*parts)

    return path


def file_mtime(path):
    t = datetime.fromtimestamp(os.stat(path).st_mtime)
    return t.strftime("%Y-%m-%d %M:%M:%S")


def print_diff(fromfile: Path, tofile: Path):
    with open(fromfile) as ff:
        fromlines = ff.readlines()
    with open(tofile) as tf:
        tolines = tf.readlines()
    fromdate = file_mtime(fromfile)
    todate = file_mtime(tofile)
    diff = difflib.unified_diff(
        fromlines, tolines, str(fromfile), str(tofile), fromdate, todate, n=3
    )
    has_diff = False
    for i in diff:
        has_diff = True
        if i.startswith("---"):
            i = Fore.RED + Style.BRIGHT + i + Style.RESET_ALL
        elif i.startswith("+++"):
            i = Fore.GREEN + Style.BRIGHT + i + Style.RESET_ALL
        elif i.startswith("-"):
            i = Fore.RED + i + Fore.RESET
        elif i.startswith("+"):
            i = Fore.GREEN + i + Fore.RESET
        elif i.startswith("@"):
            i = Fore.BLUE + i + Fore.RESET
        print("\t" + i, end="")
    return has_diff


def file_exists_in_other_higher_priority_user(path, users_list):
    user = get_user_path(path)

    index_actual_user = users_list.index(user)
    higher_level_users = users_list[index_actual_user + 1 :]
    for user in higher_level_users:
        new_path = change_user_path(path, user)
        if os.path.isfile(new_path):
            return True

    return False


def is_first_directory_bigger_than_second(first, second) -> bool:
    return os.listdir(first) > os.listdir(second)
