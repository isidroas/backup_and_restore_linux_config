import os
import click
import shutil
from pathlib import Path

from common import EXCLUDE_FOLDER, EXCLUDE_FILE, print_diff, change_user_path


@click.command(
    help="Copies files present BACKUP from the root to BACKUP. BACKUP should be like a root directory, in other words, it should contain a home folder"
)
@click.argument("backup", type=click.Path(exists=True))
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
def main(backup, selected_users, dry_run, ask_before):
    # def main(**kwargs):
    #    print(kwargs)
    #    quit()

    # Force dryrun when debugging
    dry_run = True

    # TODO: Check if backup contains "home" folder

    for directory in Path(backup).glob('**'):
        assert not directory.is_file()

        if any([e in directory.parts for e in EXCLUDE_FOLDER]):
            continue
        for file_dst in directory.iterdir():
            if file_dst.is_dir():
                continue

            if any([e in file_dst.parts for e in EXCLUDE_FILE]):
                continue

            assert file_dst.is_file()

            ####################### Handle users #######################

            #if len(selected_users) > 1 and (
            #    file_dst not in selected_users
            #    or file_exists_in_other_higher_priority_user(
            #        "/" + rel_path, selected_users
            #    )
            #):
            #    continue

            file_src = Path("/") / file_dst.relative_to(backup)
            file_src = change_user_path(file_src, os.environ["USER"])

            #############################################################


            print(f"file_src: {file_src}")
            print(f"file_dst: {file_dst}")


            if file_src.is_file():
                if not print_diff(file_src, file_dst):
                    print("Skipping copy, both files are equal")
                    continue
                if not dry_run:
                    pass
                    #shutil.copy(file_src, file_dst)
            else:
                print("Backup file does not exists in system")
                # TODO: remove file in backup?

            print("")


if __name__ == "__main__":
    main()
