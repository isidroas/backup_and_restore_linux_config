import os
import click
import shutil

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

    for root, dirs, files in os.walk(backup):
        if any([e in root for e in EXCLUDE_FOLDER]):
            continue
        for f in files:
            if any([e in f for e in EXCLUDE_FILE]):
                continue

            file_dst = os.path.join(root, f)

            ####################### Handle users #######################

            if len(selected_users) > 1 and (
                file_dst not in selected_users
                or file_exists_in_other_higher_priority_user(
                    "/" + rel_path, selected_users
                )
            ):
                continue

            file_src = "/" + os.path.relpath(file_dst, backup)
            file_src = change_user_path(file_src, os.environ["USER"])

            #############################################################


            print(f"file_src: {file_src}")
            print(f"file_dst: {file_dst}")

            exists = os.path.isfile(file_src)

            if exists:
                if not print_diff(file_src, file_dst):
                    print("Skipping copy, both files are equal")
                    continue
                if not dry_run:
                    shutil.copy(file_src, file_dst)
            else:
                print("Backup file does not exists in system")
                # TODO: remove file in backup?

            print("")


if __name__ == "__main__":
    main()
