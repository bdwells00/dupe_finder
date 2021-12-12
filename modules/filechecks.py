
from collections import defaultdict as dd
import hashlib
from betterprint.betterprint import bp
from betterprint.colortext import Ct
from modules.timer import perf_timer


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
@perf_timer
def size_comp(file_dict: dict):

    # ~~~ #                 -variables-
    size_dict, dupe_dict_stage1, data_dict = dd(list), dd(list), dd(int)

    # ~~~ #                 -dicts-
    # create dict where size is the key, and the value is a list of file names
    for k, v in file_dict.items():
        size_dict[v].append(k)
    # get a dict only containing files with matching sizes
    for k, v in size_dict.items():
        num_v = len(v)
        if num_v > 1:
            dupe_dict_stage1[k] = v
            data_dict['num_files'] += len(v)
            data_dict['num_sizes'] += 1
            data_dict['total_size'] += k * (num_v - 1)
    return dupe_dict_stage1, data_dict


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def hash_check(file: str, hash_variable):

    # ~~~ #                 -variables-
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
def hash_comp(file_dict: dict, size_dict: dict, file_count, hash_variable):

    # ~~~ #                 -variables-
    hash_dict, dupe_dict, data_dict = dd(list), dd(list), dd(int)

    # ~~~ #                 -dicts-
    # create dict where hash is the key, and the value is a list of file names
    for k, v in file_dict.items():
        for file in v:
            hash_return = hash_check(file, hash_variable)
            hash_dict[hash_return].append(file)
            data_dict['file_complete'] += 1
            bp(['\u001b[1000DHashing: ', Ct.A, f'{data_dict["file_complete"]}',
                Ct.BBLUE, '/', Ct.A, f'{file_count}', Ct.BBLUE], log=0, inl=1,
                num=0, fls=1, fil=0)
    bp(['\n', Ct.A], fil=0)
    # get a dict only containing files with matching hash
    for k, v in hash_dict.items():
        num_v = len(v)
        if num_v > 1:
            dupe_dict[k] = v
            data_dict['num_files'] += num_v
            data_dict['num_hashes'] += 1
            for i in v:
                data_dict['total_size'] += size_dict[i]
    return dupe_dict, data_dict
