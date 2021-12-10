

from collections import defaultdict as dd
import os
from betterprint.betterprint import bp
from betterprint.colortext import Ct
from modules.timer import perf_timer
from modules.options import args


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def tree_walk_error_output(os_error: str):
    """Receive errors from tree_walk function, color red, then send to output
    either just log file or both log and elog files.

    Args:
        - os_error (str): os.walk onerror output
    """
    bp([os_error, Ct.RED], erl=2)

    return


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
@perf_timer
def tree_walk(walk_folder: str):
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
        for root, dirs, files, in os.walk(walk_folder,
                                          topdown=True,
                                          onerror=tree_walk_error_output):
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
        bp([f'tree walk failure: {walk_folder}\n{e}', Ct.RED], erl=2)

    # return 101, walk_fol, walk_files, file_size, num_folders, num_files
    return walk_dirs_dict, walk_files_dict, file_size, num_files, num_dirs
