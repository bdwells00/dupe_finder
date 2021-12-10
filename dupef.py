#!/usr/bin/python3-64 -X utf8

from datetime import datetime
from time import perf_counter
from modules.argsval import validate_and_process_args, file_check
from betterprint.betterprint import bp, bp_dict
from betterprint.colortext import Ct
from modules.filechecks import size_comp, hash_comp
from modules.notations import byte_notation, time_notation
import modules.options as options
from modules.timer import perf_timer
from modules.treewalk import tree_walk
START_PROG_TIME = perf_counter()


# ~~~ #             -global variables-
start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
@perf_timer
def out_file_check(dupe_f: int, dupe_h: int):

    # ~~~ #             -question-
    if dupe_f > 30 and not args.log_file:
        o_check = input(f'Found {Ct.BBLUE}{dupe_f}{Ct.A} files that can be '
                        f'shrunk down to {Ct.BBLUE}{dupe_h}{Ct.A} files.\n\n'
                        'Dumping this many to the console might take a long '
                        'time but no log-file was specified. Do you want to '
                        f'output to {Ct.GREEN}C{Ct.A}onsole or specify '
                        f'{Ct.GREEN}L{Ct.A}og-file now?[{Ct.GREEN}C{Ct.A}/'
                        f'{Ct.GREEN}L{Ct.A}]: ')
        if o_check.lower() == 'l':
            f_temp = input('File name: ')
            file_check(f_temp)
            bp_dict['log_file'] = f_temp
        elif o_check.lower() != 'c':
            bp([f'{o_check} is not "C" or "L".', Ct.YELLOW], err=1, fil=0)
            out_file_check(dupe_f, dupe_h)
    elif dupe_f < 30:
        bp([f'Found {dupe_f} files that can be shrunk down to {dupe_h} files.'
            f'\nSending to console and {bp_dict["log_file"]}.', Ct.A])
        o_check = 'c'
    else:
        o_check = input(f'Found {Ct.BBLUE}{dupe_f}{Ct.A} files that can be '
                        f'shrunk down to {Ct.BBLUE}{dupe_h}{Ct.A} files.\n\n'
                        f'Do you want to output to {Ct.GREEN}C{Ct.A}onsole or '
                        f'just the {Ct.GREEN}L{Ct.A}og-file?[{Ct.GREEN}C{Ct.A}'
                        f'/{Ct.GREEN}L{Ct.A}]: ')
        if o_check.lower() != 'c' and o_check.lower() != 'l':
            bp([f'{o_check} is not "C" or "L".', Ct.YELLOW], err=1, fil=0)
            out_file_check(dupe_f, dupe_h)
    return o_check


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
    walk_return = tree_walk(args.folder)
    tw_tup = walk_return[2]
    folder_total = f'{tw_tup[4]:,}'
    file_total = f'{tw_tup[3]:,}'
    file_size_total = byte_notation(tw_tup[2], ntn=1)
    walk_time = f'{walk_return[1]:.4f}' if walk_return[1] < 10 else\
        time_notation(walk_return[1])
    # print out the tree walk data
    bp([f'Folders: {folder_total} | Files: {file_total} | '
        f'File Size: {file_size_total[1]:>10}\nDuration: {walk_time}', Ct.A])
    bp([f'\n{"━" * 40}\n', Ct.A], log=0)

    # ~~~ #             -size comparison-
    _, size_r_time, size_return = size_comp(tw_tup[1])
    # print(size_return[1])
    files_stage1 = size_return[1]['num_files']
    sizes_stage1 = size_return[1]['num_sizes']
    data_stage1 = size_return[1]['total_size']
    dupe_stage1 = files_stage1 - sizes_stage1
    size_time = f'{size_r_time:.4f}' if size_r_time < 10 else\
        time_notation(size_r_time)
    # print out the size comp stage 1 comparison
    bp(['Stage ', Ct.GREEN, '1', Ct.BBLUE, ' (', Ct.GREEN, 'size', Ct.RED,
        ') Comparison:\n', Ct.GREEN], num=0)
    bp([f'Files with a size match: {files_stage1:,}\nNumber of size '
        f'matches: {sizes_stage1}\nPotential duplicates: {dupe_stage1} files |'
        f' {byte_notation(data_stage1, ntn=1)[1]}\n'
        f'Duration: {size_time}', Ct.A])
    bp([f'\n{"━" * 40}\n', Ct.A], log=0)

    # ~~~ #             -sha256 comparison-
    _, sha256_r_time, sha256_return = hash_comp(size_return[0], tw_tup[1],
                                                files_stage1, 'sha256')
    files_stage2 = sha256_return[1]['num_files']
    hashes_stage2 = sha256_return[1]['num_hashes']
    data_stage2 = sha256_return[1]['total_size']
    dupe_stage2 = files_stage2 - hashes_stage2
    sha256_time = f'{sha256_r_time:.4f}' if sha256_r_time < 10 else\
        time_notation(sha256_r_time)
    # print out the hash comp stage 2 comparison
    bp(['Stage ', Ct.GREEN, '2', Ct.BBLUE, ' (', Ct.GREEN, 'sha256', Ct.RED,
        ') Comparison:\n', Ct.GREEN], num=0)
    bp([f'Files with a hash match: {files_stage2:,}\nNumber of hash '
        f'matches: {hashes_stage2}\nHash Confirmed duplicates: '
        f'{dupe_stage2} files | {byte_notation(data_stage2, ntn=1)[1]}\n'
        f'Duration: {sha256_time}', Ct.A])
    bp([f'\n{"━" * 40}\n', Ct.A], log=0)

    # ~~~ #             -blake2b comparison-
    files_stage3 = 0
    if args.two_hash:
        _, blake2b_r_time, blake2b_return = hash_comp(size_return[0],
                                                      tw_tup[1], files_stage1,
                                                      'blake2b')
        files_stage3 = blake2b_return[1]['num_files']
        hashes_stage3 = blake2b_return[1]['num_hashes']
        data_stage3 = blake2b_return[1]['total_size']
        dupe_stage3 = files_stage3 - hashes_stage3
        blake2b_time = f'{blake2b_r_time:.4f}' if blake2b_r_time < 10\
            else time_notation(blake2b_r_time)
        # print out the hash comp stage 2 comparison
        bp(['Stage ', Ct.GREEN, '3', Ct.BBLUE, ' (', Ct.GREEN, 'blake2b',
            Ct.RED, ') Comparison:\n', Ct.GREEN], num=0)
        bp([f'Files with a hash match: {files_stage3:,}\nNumber of hash '
            f'matches: {hashes_stage3}\nHash Confirmed duplicates: '
            f'{dupe_stage3} files | {byte_notation(data_stage3, ntn=1)[1]}\n'
            f'Duration: {blake2b_time}', Ct.A])
        bp([f'\n{"━" * 40}\n', Ct.A], log=0)

    # ~~~ #             -aggregate-
    hash_level = 2 if args.two_hash else 1
    if hash_level == 2 and dupe_stage3 != dupe_stage2:
        bp([f'hash mismatch!! Stage 2 found: {dupe_stage2} | Stage 3 '
            f'found: {dupe_stage3}\nUsing Stage 3 data. blake2b has no '
            'confirmed hash collisions. Data should be verified before '
            'deleted.', Ct.YELLOW], err=1)
        dupe_final = files_stage3
        dupe_hashes = hashes_stage3
        dupe_dict = blake2b_return[0]
    elif hash_level == 2 and dupe_stage3 == dupe_stage2:
        bp([f'Hash lists match. Stage 2 found: {dupe_stage2} | Stage 3 '
            f'found: {dupe_stage3}\nUsing Stage 3 data with maximum '
            'confidence.', Ct.GREEN])
        dupe_final = files_stage3
        dupe_hashes = hashes_stage3
        dupe_dict = blake2b_return[0]
    else:
        bp([f'Stage 2 found: {dupe_stage2}\nUsing Stage 2 data with '
            'high confidence.', Ct.GREEN])
        dupe_final = files_stage2
        dupe_hashes = hashes_stage2
        dupe_dict = sha256_return[0]
    bp([f'\n{"━" * 40}\n', Ct.A], log=0)

    # ~~~ #             -input-
    if args.auto:
        con_out = 0
    else:
        input_return = out_file_check(dupe_final, dupe_hashes)
        if input_return[2].lower() == 'l':
            con_out = 0
        else:
            con_out = 1
        bp([f'\n{"━" * 40}\n', Ct.A], log=0, fil=0)

    # ~~~ #             -output-
    bp([f'Files with duplicates: {dupe_hashes} | Total duplicates: '
        f'{dupe_final - dupe_hashes}\n', Ct.A], con=con_out)
    for k, v in dupe_dict.items():
        bp([f'{k}', Ct.A], num=0, con=con_out)
        for entry in v:
            bp([f'\t{entry}', Ct.GREEN], con=con_out)
    bp([f'\n{"━" * 40}\n', Ct.A], log=0, con=con_out)

    # ~~~ #             -finish-
    total_time = (perf_counter() - START_PROG_TIME - input_return[1])
    if total_time > 10:
        total_time = time_notation(total_time)
    bp(['Program complete\n\nDuration: '
        f'{perf_counter() - START_PROG_TIME - input_return[1]:.4f}', Ct.A])


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
if __name__ == '__main__':

    # ~~~ #             -args-
    args = options.args

    # ~~~ #             -title-
    bp([f'{options.ver} - {options.purpose}\n', Ct.BBLUE])

    # ~~~ #             -validate-
    fc_return = validate_and_process_args()

    # ~~~ #             -variables-
    bp_dict['color'] = 0 if args.no_color else 1
    bp_dict['log_file'] = fc_return if fc_return else args.log_file

    main()
