
import os
import sys
from betterprint.betterprint import bp
from betterprint.colortext import Ct
from modules.options import args


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def yn_question():
    """Confirm exit.

    - Returns:
        - [str]: 'y' to exit, 'n' for no
    """
    yn_return = input(f'{Ct.RED}Are you sure? This will hard exit without '
                      f'saving. [Y/N]: {Ct.A}')
    if yn_return.lower() == 'x':
        return 'y'
    elif yn_return.lower() == 'y':
        return 'y'
    elif yn_return.lower() == 'n':
        return 'n'
    else:
        bp([f'{yn_return} is neither "Y" nor "N".', Ct.YELLOW])
        yn_question()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def new_file():
    """Simple input question for file output."""
    return input('Please provide a new file for output: ')


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def check_new_file():
    """Ask for new filename or exit. Return the new filename.

    - Returns:
        - [str]: new filename
    """
    check_new = input(f'{Ct.YELLOW}Provide a new file or exit this '
                      'application? [F/X]: '
                      f'{Ct.A}')
    # if new file, ask for the file name and check it
    if check_new.lower() == 'f':
        new_f = new_file()
        file_check(new_f)
        return new_f
    # hard exit the program
    elif check_new.lower() == 'x':
        yn_return = yn_question()
        if yn_return.lower() == 'y':
            sys.exit(0)
        else:
            check_new_file()
    # re-ask if neither n nor x
    else:
        bp([f'"{check_new}" is neither "N" nor "X". Retry.', Ct.A])
        check_new_file()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def file_check(f: str, action='append'):
    """Checks if file exists. Should an existing file be overridden, or a new
    filename provided? Or exit the application.

    - Args:
        - f (str): file to check

    - Returns:
        - [type]: returns either the original filename or a new filename
    """
    # verify valid file
    if len(f) > 0:
        if os.path.isfile(f):
            check_append = input(f'{Ct.YELLOW}({f}) exists. {action}? [Y/N]: '
                                 f'{Ct.A}')
            # ask for a new filename or exit
            if check_append.lower() == 'n':
                new_f = check_new_file()
                return new_f
            # re-ask this question due to invalid answer
            elif check_append.lower() != 'y':
                bp([f'"{check_append}" is neither "N" nor "X". Retry.', Ct.A])
                file_check(f)
            # yes to overwrite, return this filename
            else:
                return f
        # invalid file, ask for new file or exit
        else:
            return f
    else:
        bp(['No file specified.', Ct.YELLOW])
        new_f = check_new_file()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def folder_validation(f, location):
    """Check if the folder exists. Exit if it does not.

    - Args:
        - f (string): folder name in string format
        - location (string): location is proper args string
    """
    if not os.path.isdir(f):
        bp([f'"--{location} {f}" does not exist.', Ct.RED], erl=2)
        sys.exit(1)
    return


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def validate_and_process_args():
    """Validate the arparse args"""
    # ~~~ #                 -dict-
    return_dict = {
        'log_file': '',
        'json_input': '',
        'json_output': ''
    }

    # ~~~ #                 -folder validation-
    if args.folder:
        folder_validation(args.folder, 'folder')
    else:
        bp(['target path not provided.', Ct.RED], err=2)
        sys.exit(1)

    # ~~~ #                 -file validation-
    if args.log_file:
        return_dict['log_file'] = file_check(args.log_file)
    # TODO duplicate question as it is asked in jsonfinder.py. remove?
    # if args.json_output:
    #     return_dict['json_output'] = file_check(args.json_output,
    #                                             action='overwrite')

    # ~~~ #                 -input validation-
    if args.json_input:
        if not os.path.isfile(args.json_input):
            bp([f'{args.json_input} JSON file does not exist. Exiting.',
                Ct.RED], err=2)
            sys.exit(1)
        else:
            return_dict['json_input'] = args.json_input

    return return_dict
