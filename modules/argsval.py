
import os
import sys
from betterprint.betterprint import bp
from betterprint.colortext import Ct
from modules.options import args


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def new_file():

    return input('Please provide a new file for output: ')


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def file_check(f: str):

    if os.path.isfile(f):
        check_append = input(f'{Ct.YELLOW}({f}) exists. Append? [Y/N]: {Ct.A}')
        if check_append.lower() == 'n':
            check_new = input(f'{Ct.YELLOW}Provide a new file or exit? [N/X]: '
                              f'{Ct.A}')
            if check_new.lower() == 'n':
                new_f = new_file()
                file_check(new_f)
                return new_f
            elif check_new.lower() == 'x':
                sys.exit(0)
            else:
                bp([f'"{check_new}" is neither "N" nor "x". Retry.', Ct.A])
                file_check(f)
        elif check_append.lower() != 'y':
            bp([f'"{check_append}" is neither "N" nor "x". Retry.', Ct.A])
            file_check(f)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def folder_validation(f, location):
    """Check if the folder exists. Exit if it does not.

    Args:
        f (string): folder name in string format
        location (string): 'source' or 'target' being checked to provide
                           proper error output.
    """
    if not os.path.isdir(f):
        bp([f'"--{location} {f}" does not exist.', Ct.RED], erl=2)
        sys.exit(1)
    return


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def validate_and_process_args():
    """Validate the arparse args"""
    # ~~~ #         folder validation section
    if args.folder:
        folder_validation(args.folder, 'folder')
    else:
        bp(['target path not provided.', Ct.RED], err=2)
        sys.exit(1)

    # ~~~ #         log file validation
    if args.log_file:
        file_return = file_check(args.log_file)

    return file_return
