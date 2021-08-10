import os
import shutil
from typing import Tuple

import difflib
from datetime import datetime
from colorama import Fore, Style
import click
from datetime import datetime

#REPO = "./src/"
EXCLUDE_FOLDER = [".git", ".mypy_cache"]
EXCLUDE_FILE = ["TODO.md", ".swp"]
#BACKUP_DIR = "./backup2"


def get_user_path(path: str) -> str:
    list_ = path.split("/")

    if list_[1]!='home':
        raise ValueError(f"path: {path} is not an absolute path")

    return list_[2]

def change_user_path(path: str, new_user: str) -> str:
    """ Change user name of the path. The given path shoud be absolute and
    therefore the user name is in the second position (after 'home' folder)

    >>> change_user_of_path('/home/foo/.local/bin/myprogram.sh', 'bar')
    '/home/bar/.local/bin/myprogram.sh'
    """
    list_ = path.split("/")

    if list_[1]!='home':
        raise ValueError(f"path: {path} is not an absolute path")

    list_[2] = new_user
    path = "/".join(list_)
    return path

def file_mtime(path):
    t = datetime.fromtimestamp(os.stat(path).st_mtime)
    return t.strftime("%Y-%m-%d %M:%M:%S")

def print_diff(fromfile: str, tofile: str):
    with open(fromfile) as ff:
        fromlines = ff.readlines()
    with open(tofile) as tf:
        tolines = tf.readlines()
    fromdate = file_mtime(fromfile)
    todate = file_mtime(tofile)
    diff = difflib.unified_diff(fromlines, tolines, fromfile, tofile, fromdate, todate, n=3)
    has_diff = False
    for i in diff:
        has_diff = True
        if i.startswith('---'):
            i = Fore.RED + Style.BRIGHT + i + Style.RESET_ALL
        elif i.startswith('+++'):
            i = Fore.GREEN + Style.BRIGHT + i + Style.RESET_ALL
        elif i.startswith('-'):
            i = Fore.RED + i + Fore.RESET
        elif i.startswith('+'):
            i = Fore.GREEN + i + Fore.RESET
        elif i.startswith('@'):
            i = Fore.BLUE + i + Fore.RESET
        print('\t'+ i, end='')
    return has_diff

def file_exists_in_other_higher_priority_user(path, users_list):
    user = get_user_path(path)
    

    index_actual_user = users_list.index(user)
    higher_level_users = users_list[index_actual_user+1:]
    for user in higher_level_users:
        new_path = change_user_path(path, user) 
        if os.file_exists(new_path):
            return True
    
    return False

def is_first_directory_bigger_than_second(first, second) -> bool:
    return os.listdir(first) > os.listdir(second)




@click.command(help= "Copies contents from SOURCE to DESTINATION, only the files present in FILES_TO_TRACK. Booth directories should be like a root directory, in other words, they should contain a home folder")
@click.argument('source', type=click.Path(exists=True))
@click.argument('destination', type=click.Path(exists=False))
@click.option('--back-up', type=click.Path(exists=True), default='./', help = "folder where backup will be saved. It will create a folder with a timestamp: 'backup_%Y-%m-%d_%H:%M:%S'. Only files that were overwritten will be saved. It default location is the home folder (or the current directory?). This is useful when a disaster occurs after apply the backup")
@click.option('--iteration-users', multiple=True, type=str, help= "list of users. When the same file appear in different users, the first has priority")
@click.option('--dry-run', is_flag=True)
@click.option('--ask-before', is_flag=True, help="if the file already exists, show the diff and ask whether overwrite.")
@click.option('--copy-all-from-source', is_flag=True, help="Copy all the files from source directory to destination directory, not only them which are present in both")
def main(source, destination, back_up, iteration_users, dry_run, ask_before, copy_all_from_source):
#def main(**kwargs):
    #print(kwargs)
    #quit()
    # Force dryrun when debugging
    dry_run=True
    iterate_over_source = is_first_directory_bigger_than_second(destination, source)
    if iterate_over_source:
        iteration_directory = source
        other_directory = destination
    else: 
        iteration_directory = destination
        other_directory = source

    generic_user = 'isidro'

    # TODO: Check if src and dst contains "home" folder

#    if back_up:
#        back_up_timestamp = os.path.join(back_up, datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))


    for root, dirs, files in os.walk(iteration_directory):
        if any([e in root for e in EXCLUDE_FOLDER]):
            continue
        for f in files:
            if any([e in f for e in EXCLUDE_FILE]):
                continue

            file = os.path.join(root,f)
            rel_path = '/' +  os.path.relpath(file, iteration_directory)
            if len(iteration_users)>1 and (file not in iteration_users or file_exists_in_other_higher_priority_user('/' + rel_path,iteration_users)):
                    continue

            # TODO: add prefix because other directory won't be always '/'
#            file_other = other_directory + change_user_path(rel_path, generic_user)
            file_other = change_user_path(rel_path, generic_user)

            if iterate_over_source:
                file_src = file
                file_dst = file_other 
            else:
                file_src = file_other
                file_dst = file

            print(f"file_src: {file_src}")
            print(f"file_dst: {file_dst}")

            exists = os.path.isfile(file_other)
    
            if exists:
                if not print_diff(file_src, file_dst):
                    print("Skipping copy, both files are equal")
                    continue
                # TODO: backup
            else:
                if not dry_run:
                    os.makedirs(os.path.dirname(file_other), exist_ok=True)
            if not dry_run:
                shutil.copy(file_src, file_dst)

            print("")


if __name__=="__main__":
    main()
    
