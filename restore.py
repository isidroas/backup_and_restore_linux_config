import os
import click
import shutil

from pathlib import Path

from common import EXCLUDE_FOLDER, EXCLUDE_FILE, print_diff, change_user_path


@click.command(
    help="Copies contents from BACKUP to the root using the actual user. BACKUP should be like a root directory, in other words, it should contain a home folder"
)
@click.argument("backup", type=click.Path(exists=True))
@click.option(
    "--overwritten-backup",
    type=click.Path(exists=True),
    default="./",
    help="folder where backup will be saved. It will create a folder with a timestamp: 'backup_%Y-%m-%d_%H:%M:%S'. Only files that were overwritten will be saved. It default location is the home folder (or the current directory?). This is useful when a disaster occurs after apply the backup",
)
@click.option(
    "--selected-users",
    multiple=True,
    type=str,
    help="list of users to copy. All specified users should be present in the directory 'BACKUP/home'. When the same file appear in different users, the first has priority",
)
@click.option("--dry-run", is_flag=True)
@click.option(
    "--ask-before",
    is_flag=True,
    help="if the file already exists, show the diff and ask whether overwrite.",
)
def main(backup, overwritten_backup, selected_users, dry_run, ask_before):
    # def main(**kwargs):
    #    print(kwargs)
    #    quit()

    # Force dryrun when debugging
    dry_run = True

    # TODO: Check if backup contains "home" folder

    #    if overwritten_backup:
    #        back_up_timestamp = os.path.join(back_up, datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))

    # TODO: use Path.glob('*')
#    for root, dirs, files in os.walk(backup):
    for directory in Path(backup).glob('**'):
        if any([e in directory.parts for e in EXCLUDE_FOLDER]):
            continue
#        for f in files:
        for file_src in directory.glob('*'):
            if any([e in file_src.parts for e in EXCLUDE_FILE]):
                continue

            assert file_src.is_file()
            ####################### Handle users #######################

            #file_src = Path(root) / f
#            if len(selected_users) > 1 and (
#                file_src not in selected_users
#                or file_exists_in_other_higher_priority_user(
#                    "/" + rel_path, selected_users
#                )
#            ):
#                continue

            file_dst = Path("/") / file_src.relative_to(backup)
            file_dst = change_user_path(file_dst, os.environ["USER"])

            #############################################################

            print(f"file_src: {file_src}")
            print(f"file_dst: {file_dst}")

            if file_dst.is_file():
                if not print_diff(file_src, file_dst):
                    print("Skipping copy, both files are equal")
                    continue
                # TODO: backup
            else:
                if not dry_run:
                    pass
                    #os.makedirs(os.path.dirname(file_dst), exist_ok=True)
            if not dry_run:
                pass
                #shutil.copy(file_src, file_dst)

            print("")


if __name__ == "__main__":
    main()
