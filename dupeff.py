#!/usr/bin/env python3

from datetime import datetime, timedelta
from math import ceil
from time import perf_counter
from betterprint.betterprint import bp, bp_dict
from betterprint.colortext import Ct
from modules.argsval import validate_and_process_args
from modules.filedelete import expiramental_file_deletion
from modules.jsonfinder import save_json, import_json
from modules.livefinder import live_duplicate_finder, out_file_check
import modules.options as options
START_PROG_TIME = perf_counter()


# ~~~ #                     -global variables-
start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def del_check():
    """Interactive input section to confirm cutomer wants to delete files even
    though that is an expiramental feature.

    Returns:
        [string]: returns either 'y', 'n', or 'x'
    """
    # ~~~ #                 -input-
    del_input = input('Proceed with interactive duplicate file removal? [Y/N]:'
                      ' ')
    if del_input.lower() == 'y':
        return del_input
    elif del_input.lower() == 'x':
        return 'n'
    elif del_input.lower() != 'n':
        bp([f'{del_input} is neither "Y" nor "N".', Ct.YELLOW])
        del_check()
    else:
        return del_input


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def main():

    # ~~~ #                 -initial display-
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

    # ~~~ #                 -live or json-
    if args.json_input:
        dr_dict = import_json()
    else:
        dr_dict = live_duplicate_finder()

    # ~~~ #                 -variables-
    # keep output variables in a single dict
    out_dict = {
        'dupe_dict': dr_dict['dupe_dict'],
        'dupe_files': dr_dict['dupe_files'],
        'dupe_hashes': dr_dict['dupe_hashes'],
        'del_dict': dr_dict['dupe_dict'],
        'del_time': 0.0,
        'del_files': 0,
        'del_hashes': 0,
        'remaining_files': 0,
        'remaining_hashes': 0
    }

    # ~~~ #                 -file deletion-
    if args.enable_delete_files and dr_dict['dupe_files'] > 0:
        bp([f'{"*" * 50}\n* WARNING: FILE DELETION MODE IS EXPIRAMENTAL!!! *\n'
            f'{"*" * 50}\n\nUse with caution.\nThis might delete the wrong '
            'file or cause other irreparable harm.\nYou can exit file deletion'
            'any time by pressing "X" or "CTRL + C"\n', Ct.RED])
        del_check_return = del_check()
        if del_check_return.lower() == 'y':
            # delete files
            del_return = expiramental_file_deletion(dr_dict['dupe_dict'])
            out_dict['del_time'] = del_return[1]
            bp([f'Duration: {out_dict["del_time"]}', Ct.A])
            out_dict['del_dict'] = del_return[2]
            for k, v in out_dict['del_dict'].items():
                if len(v) > 1:
                    out_dict['remaining_files'] += len(v)
                    out_dict['remaining_hashes'] += 1
                else:
                    out_dict['remaining_files'] += 1
                    out_dict['remaining_hashes'] += 1

            out_dict['del_files'] = dr_dict['dupe_files'] - \
                out_dict['remaining_files']
            out_dict['del_hashes'] = dr_dict['dupe_hashes'] - \
                out_dict['remaining_hashes']
        else:
            bp(['Expiramental file deletion skipped.', Ct.A])
        bp([f'\n{"━" * 40}\n', Ct.A], log=0)

    # ~~~ #                 -input-
    if args.auto:
        con_out = 0
    else:
        input_return = out_file_check(out_dict)
        if input_return[2].lower() == 'l':
            con_out = 0
        else:
            con_out = 1
        bp([f'\n{"━" * 40}\n', Ct.A], log=0, fil=0)

    # ~~~ #                 -output-
    # reprocess in case of deletions
    duplicates = out_dict["dupe_files"] - out_dict["dupe_hashes"]
    bp([f'Found duplicates: {duplicates} | Deleted duplicates: '
        f'{out_dict["del_files"]}\n\nDuplicates remaining: '
        f'{duplicates - out_dict["del_files"]}', Ct.A],
        con=con_out)
    for k, v in out_dict['del_dict'].items():
        if len(v) > 1:
            bp([f'{k}', Ct.A], num=0, con=con_out)
            for entry in v:
                bp([f'\t{entry}', Ct.GREEN], num=0, con=con_out)
    bp([f'\n{"━" * 40}\n', Ct.A], log=0, con=con_out)

    # ~~~ #                 -json output-
    if args.json_output:
        save_json(out_dict['del_dict'], options.json_output)

    # ~~~ #                 -finish-
    total_time = (perf_counter() - START_PROG_TIME)
    program_time = total_time - input_return[1] - out_dict['del_time']
    bp(['Program complete\n\n'
        f'{timedelta(seconds=ceil(total_time))} - Total Duration\n'
        f'{timedelta(seconds=ceil(input_return[1]))} - Input Time\n'
        f'{timedelta(seconds=ceil(out_dict["del_time"]))} - Deletion Time\n'
        f'{timedelta(seconds=ceil(program_time))} - Program Overhead Time',
        Ct.A])


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
if __name__ == '__main__':

    # ~~~ #                 -args-
    args = options.args

    # ~~~ #                 -title-
    bp([f'{options.ver} - {options.purpose}\n', Ct.BBLUE])

    # ~~~ #                 -validate-
    val_args_dict = validate_and_process_args()

    # ~~~ #                 -variables-
    bp_dict['color'] = 0 if args.no_color else 1
    bp_dict['log_file'] = val_args_dict['log_file']
    options.json_input = val_args_dict['json_input']
    options.json_output = val_args_dict['json_output']

    main()
