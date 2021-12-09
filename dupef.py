#!/usr/bin/python3-64 -X utf8

__author__ = 'Brandon Wells <wellsb.prog@gmail.com>'
__license__ = 'MIT'
__origin_date__ = '2021-12-09'
__prog__ = 'dupef.py'
__purpose__ = 'duplicate finder: find duplicate files in a folder tree'
__version__ = '0.0.2'
__version_date__ = '2021-12-09'
__version_info__ = tuple(int(i) for i in __version__.split('.') if i.isdigit())


import argparse
from collections import defaultdict as dd
from datetime import datetime
from functools import wraps
import hashlib
from time import perf_counter
import os
import sys
from betterprint.betterprint import bp, bp_dict
from betterprint.colortext import Ct
START_PROG_TIME = perf_counter()


# ~~~ #             -global variables-
ver = f'{__prog__} v{__version__} ({__version_date__})'
start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def get_args():
    """Get CLI arguments from argparse.

    Returns:
        - class 'argparse.ArgumentParser': Command Line Arguments
    """
    # Use argparse to capture cli parameters
    parser = argparse.ArgumentParser(
        prog=__prog__,
        description=f'{Ct.BBLUE}{ver}: {__purpose__}{Ct.A}',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog=f'{Ct.RED}This program has no warranty. Please use with '
               f'caution.{Ct.A}',
        add_help=True)
    parser.add_argument('-f',
                        '--folder',
                        help='folder to scan for duplicates',
                        metavar=f'{Ct.RED}<path>{Ct.A}',
                        type=str)
    parser.add_argument('--exdir',
                        help='comma separated directories to exclude (no '
                             'spaces between directories)',
                        metavar=f'{Ct.GREEN}<dir>,<dir>{Ct.A}',
                        type=str)
    parser.add_argument('--exfile',
                        help='comma separated files to exclude (no spaces '
                             'between files)',
                        metavar=f'{Ct.GREEN}<file>,<file>{Ct.A}',
                        type=str)
    parser.add_argument('--log-file',
                        help='file to save output',
                        metavar=f'{Ct.GREEN}<filename>{Ct.A}',
                        type=str)
    parser.add_argument('--no-color',
                        help='don\'t colorize output',
                        action='store_true')
    parser.add_argument('--two-hash',
                        help='also hash with blake2b for increased accuracy',
                        action='store_true')
    parser.add_argument('--version',
                        help='print program version and exit',
                        action='version',
                        version=f'{ver}')

    return parser.parse_args()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def validate_args():

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
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
    if args.folder:
        folder_validation(args.folder, 'folder')
    else:
        bp(['target path not provided.', Ct.RED], err=2)
        sys.exit(1)
    if args.log_file:
        if os.path.isfile(args.log_file):
            bp(['log file exists. Exiting.', Ct.RED], err=2)
            sys.exit(1)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def perf_timer(func):
    """The decorator time function. This is the encapsulating timer
        functionthat takes one argument, the child function, to calculate the
        duration of time.

    - Args:
        - child_function ([function]): the child function to execute

    - Return:
        - wrapper_function: tuple
            - 0: child function name
            - 1: duration the time function ran using time.perf_counter_ns
            - 2: the child function return
    """
    # ~~~ #         timer function section
    # using functools.wraps to pass along the child_function details
    @wraps(func)
    def wrapper_function(*args, **kwargs):
        """The decorator time function. This is the encapsulating timer
         functionthat takes one argument, the child function, to calculate the
         duration of time.

        - Args:
            - child_function ([function]): the child function to execute

        - Return:
            - wrapper_function: tuple
                - 0: child function name
                - 1: duration the time function ran using time.monotonic
                - 2: the child function return
        """
        t_start = perf_counter()
        return_var = func(*args, **kwargs)
        t_required = perf_counter() - t_start
        return func.__name__, t_required, return_var
    return wrapper_function


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def byte_notation(size: int, acc=2, ntn=0):
    """Decimal Notation: take an integer, converts it to a string with the
    requested decimal accuracy, and appends either single (default), double,
    or full word character notation.

    - Args:
        - size (int): the size to convert
        - acc (int, optional): number of decimal places to keep. Defaults to 2.
        - ntn (int, optional): notation name length. Defaults to 0.

    - Returns:
        - [tuple]: 0 = original size int unmodified; 1 = string for printing
    """
    size_dict = {
        1: ['B', 'B', 'bytes'],
        1000: ['k', 'kB', 'kilobytes'],
        1000000: ['M', 'MB', 'megabytes'],
        1000000000: ['G', 'GB', 'gigabytes'],
        1000000000000: ['T', 'TB', 'terabytes']
    }
    return_size_str = ''
    for key, value in size_dict.items():
        if (size / key) < 1000:
            return_size_str = f'{size / key:,.{acc}f} {value[ntn]}'
            return size, return_size_str


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
@perf_timer
def tree_walk():
    """Tree walks the source folder and populates several variables

    Returns:
        - tuple:
            - walk_time:      float of time it took to tree walk
            - walk_folders:   list of folders from the tree walk
            - walk_files:     list of files from the tree walk
            - data_size:      total size of all files
    """
    try:
        walk_dirs_dict, walk_files_dict = dd(int), dd(int)
        file_size, num_dirs, num_files = 0, 0, 0
        # create exdir and exfile lists
        if args.exdir:
            exdir = args.exdir.split(',')
        if args.exfile:
            exfile = args.exfile.split(',')
        for root, dirs, files, in os.walk(args.folder, topdown=True):
            # strip excluded directories and files
            if args.exdir:
                dirs[:] = [d for d in dirs if d not in exdir]
            if args.exfile:
                files[:] = [f for f in files if f not in exfile]
            # populate the directory list
            for d in dirs:
                dir_fullpath = os.path.join(root, d)
                walk_dirs_dict[dir_fullpath] = os.stat(dir_fullpath).st_size
                num_dirs += 1
            # poopulate the file list
            for f in files:
                file_fullpath = os.path.join(root, f)
                walk_files_dict[file_fullpath] = os.stat(file_fullpath).st_size
                num_files += 1
                file_size += os.stat(file_fullpath).st_size
    except OSError as e:
        bp([f'tree walk failure: {args.folder}\n{e}', Ct.RED], erl=2)

    # return 101, walk_fol, walk_files, file_size, num_folders, num_files
    return walk_dirs_dict, walk_files_dict, file_size, num_files, num_dirs


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
@perf_timer
def size_comp(file_dict: dict):

    # ~~~ #             -variables-
    size_dict, dupe_dict_stage1 = dd(list), dd(list)
    num_files, num_sizes = 0, 0

    # ~~~ #             -dicts-
    # create dict where size is the key, and the value is a list of file names
    for k, v in file_dict.items():
        size_dict[v].append(k)
    # get a dict only containing files with matching sizes
    for k, v in size_dict.items():
        if len(v) > 1:
            dupe_dict_stage1[k] = v
            num_files += len(v)
            num_sizes += 1
    return dupe_dict_stage1, num_files, num_sizes


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def hash_check(file: str, hash_variable):

    # ~~~ #             -variables-
    hf_var = (getattr(hashlib, hash_variable)())
    try:
        with open(file, 'rb') as f:
            while True:
                f_chunk = f.read(100000)
                if not f_chunk:
                    break
                hf_var.update(f_chunk)
        return hf_var.hexdigest()
    except OSError as e:
        bp([f'with file {file}.\n{e}', Ct.RED], erl=2)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
@perf_timer
def hash_comp(file_dict: dict, file_count, hash_variable):

    # ~~~ #             -variables-
    hash_dict, dupe_dict_stage2 = dd(list), dd(list)
    num_files, num_hashes, file_complete = 0, 0, 0

    # ~~~ #             -dicts-
    # create dict where hash is the key, and the value is a list of file names
    for _, v in file_dict.items():
        for file in v:
            hash_return = hash_check(file, hash_variable)
            hash_dict[hash_return].append(file)
            file_complete += 1
            bp(['\u001b[1000DHashing: ', Ct.A, f'{file_complete}', Ct.BBLUE,
                '/', Ct.A, f'{file_count}', Ct.BBLUE], log=0, inl=1, num=0,
                fls=1, fil=0)
    bp(['\n', Ct.A], fil=0)
    # get a dict only containing files with matching hash
    for k, v in hash_dict.items():
        if len(v) > 1:
            dupe_dict_stage2[k] = v
            num_files += len(v)
            num_hashes += 1

    return dupe_dict_stage2, num_files, num_hashes


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def main():

    # ~~~ #             -initial display-
    bp([f'Program start: {start_time}\nFolder: ', Ct.A, f'{args.folder}\n',
        Ct.GREEN, 'Excluded Folders: ', Ct.A, f'{args.exdir}\n', Ct.GREEN,
        'Excluded Files: ', Ct.A, f'{args.exfile}', Ct.GREEN])
    bp(['Args: ', Ct.A], inl=1)
    for k, v in vars(args).items():
        if k != 'folder' and k != 'exdir' and k != 'exfile' and k != \
                'available':
            if k == 'hash':
                bp([f' {k}: ', Ct.A, f'{v}', Ct.RED, ' |', Ct.A], num=0,
                    inl=1, log=0)
            else:
                bp([f' {k}: {v} |', Ct.A], inl=1, log=0)
    bp([f'\n\n{"━" * 40}\n', Ct.A], log=0)

    # ~~~ #             -tree walk-
    walk_return = tree_walk()
    tw_tup = walk_return[2]
    folder_total = f'{tw_tup[4]:,}'
    file_total = f'{tw_tup[3]:,}'
    file_size_total = byte_notation(tw_tup[2], ntn=1)
    # print out the tree walk data
    bp([f'Folders: {folder_total} | File Size: {file_size_total[1]:>10} | '
        f'Files: {file_total}\nDuration: {walk_return[1]:,.4f}', Ct.A], inl=1)
    bp([f'\n\n{"━" * 40}\n', Ct.A], log=0)

    # ~~~ #             -size comparison-
    size_return = size_comp(tw_tup[1])
    files_stage1_total = size_return[2][1]
    sizes_stage1_total = size_return[2][2]
    # print out the size comp stage 1 comparison
    bp(['Stage 1 (size) Comparison:\n', Ct.GREEN, 'Total sizes with file '
        f'matches: {sizes_stage1_total:,}\nTotal files with size matches: '
        f'{files_stage1_total}\nDuration: {size_return[1]:,.4f}', Ct.A], inl=1)
    bp([f'\n\n{"━" * 40}\n', Ct.A], log=0)

    # ~~~ #             -sha256 comparison-
    sha256_return = hash_comp(size_return[2][0], files_stage1_total, 'sha256')
    files_stage2_total = sha256_return[2][1]
    hashes_stage2_total = sha256_return[2][2]
    # print out the hash comp stage 2 comparison
    bp(['Stage ', Ct.GREEN, '2', Ct.BBLUE, ' (', Ct.GREEN, 'sha256', Ct.RED,
        ') Comparison:\n', Ct.GREEN], num=0)
    bp([f'Total hashes with file matches: {hashes_stage2_total:,}\n'
        f'Total files with hash matches: '
        f'{files_stage2_total}\nDuration: {sha256_return[1]:,.4f}', Ct.A],
        inl=1)
    bp([f'\n\n{"━" * 40}\n', Ct.A], log=0)

    # ~~~ #             -blake2b comparison-
    if args.two_hash:
        blake2b_return = hash_comp(size_return[2][0], files_stage1_total,
                                   'blake2b')
        files_stage3_total = blake2b_return[2][1]
        hashes_stage3_total = blake2b_return[2][2]
        # print out the hash comp stage 2 comparison
        bp(['Stage ', Ct.GREEN, '3', Ct.BBLUE, ' (', Ct.GREEN, 'blake2b',
            Ct.RED, ') Comparison:\n', Ct.GREEN], num=0)
        bp([f'Total hashes with file matches: {hashes_stage3_total:,}\nTotal '
            f'files with hash matches: {files_stage3_total}\nDuration: '
            f'{blake2b_return[1]:,.4f}', Ct.A], inl=1)
        bp([f'\n\n{"━" * 40}\n', Ct.A], log=0)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
if __name__ == '__main__':

    # ~~~ #         args section
    args = get_args()
    validate_args()

    # ~~~ #             -variables-
    bp_dict['color'] = 0 if args.no_color else 1
    bp_dict['log_file'] = args.log_file

    # ~~~ #         title section
    bp([f'{ver} - {__purpose__}\n', Ct.BBLUE])

    main()
