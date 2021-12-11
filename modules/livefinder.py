
from betterprint.betterprint import bp, bp_dict
from betterprint.colortext import Ct
from modules.argsval import file_check
from modules.filechecks import size_comp, hash_comp
from modules.notations import byte_notation, time_notation
from modules.options import args
from modules.timer import perf_timer
from modules.treewalk import tree_walk


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
@perf_timer
def out_file_check(out_dict: dict):

    # ~~~ #             -question-
    if out_dict['remaining_files'] > 30 and not args.log_file:
        o_check = input(f'Found {Ct.BBLUE}{out_dict["remaining_files"]}{Ct.A} '
                        f'files that can be shrunk down to {Ct.BBLUE}'
                        f'{out_dict["remaining_hashes"]}{Ct.A} files.\n\n'
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
            out_file_check(out_dict['remaining_files'],
                           out_dict["remaining_hashes"])
    elif out_dict['remaining_files'] < 30:
        bp([f'Found {out_dict["remaining_files"]} files that can be shrunk '
            f'down to {out_dict["remaining_hashes"]} files.\nSending to '
            f'console and {bp_dict["log_file"]}.', Ct.A])
        o_check = 'c'
    else:
        o_check = input(f'Found {Ct.BBLUE}{out_dict["remaining_files"]}{Ct.A} '
                        f'files that can be shrunk down to {Ct.BBLUE}'
                        f'{out_dict["remaining_hashes"]}{Ct.A} files.\n\n'
                        f'Do you want to output to {Ct.GREEN}C{Ct.A}onsole or '
                        f'just the {Ct.GREEN}L{Ct.A}og-file?[{Ct.GREEN}C{Ct.A}'
                        f'/{Ct.GREEN}L{Ct.A}]: ')
        if o_check.lower() != 'c' and o_check.lower() != 'l':
            bp([f'{o_check} is not "C" or "L".', Ct.YELLOW], err=1, fil=0)
            out_file_check(out_dict["remaining_files"],
                           out_dict["remaining_hashes"])
    return o_check


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def live_duplicate_finder():
    # ~~~ #             -tree walk-
    bp(['Stage ', Ct.GREEN, '0', Ct.BBLUE, ' (', Ct.GREEN, 'scan', Ct.RED,
        ') Tree Walk:\n', Ct.GREEN], num=0)

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
        dupe_files = files_stage3
        dupe_hashes = hashes_stage3
        dupe_dict = blake2b_return[0]
    elif hash_level == 2 and dupe_stage3 == dupe_stage2:
        bp([f'Hash lists match. Stage 2 found: {dupe_stage2} | Stage 3 '
            f'found: {dupe_stage3}\nUsing Stage 3 data with maximum '
            'confidence.', Ct.GREEN])
        dupe_files = files_stage3
        dupe_hashes = hashes_stage3
        dupe_dict = blake2b_return[0]
    else:
        bp([f'Stage 2 found: {dupe_stage2}\nUsing Stage 2 data with '
            'high confidence.', Ct.GREEN])
        dupe_files = files_stage2
        dupe_hashes = hashes_stage2
        dupe_dict = sha256_return[0]
    bp([f'\n{"━" * 40}\n', Ct.A], log=0)

    return_dict = {
        'dupe_dict': dupe_dict,
        'dupe_files': dupe_files,
        'dupe_hashes': dupe_hashes
    }
    return return_dict
