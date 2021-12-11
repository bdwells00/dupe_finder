
import os
from betterprint.betterprint import bp
from betterprint.colortext import Ct
from modules.filechecks import hash_check
from modules.jsonfinder import save_json
from modules.timer import perf_timer


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def yn_question():
    yn_return = input('Are you sure? [Y/N}: ')
    if yn_return.lower() == 'x':
        return 'y'
    elif yn_return.lower() == 'y':
        return 'y'
    elif yn_return.lower() == 'n':
        return 'n'
    else:
        bp([f'{yn_return} is neither "Y" nor "N".', Ct.YELLOW])
        yn_return()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def del_file(file: str):

    # ~~~ #             -variables-
    return_dict = {'file': file, 'success': 0}
    # ~~~ #             -delete-
    try:
        # bp([f'\nA delete request of {file} received. This action does not '
        #     'currently work but claims success.', Ct.A])
        if os.path.isfile(file):
            # bp([f'\nConfirmed {file} exists.', Ct.A])
            os.remove(file)
            return_dict['success'] = 1
            return return_dict
        else:
            bp([f'Could not find file {file}. Skip this file.', Ct.YELLOW])
            return_dict['success'] = 0
            return_dict
    except OSError as e:
        bp([f'trying to delete file.\n\t{e}\n', Ct.RED], err=2)
        return return_dict


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def dict_hex_finder(return_dict: dict):

    hex_val, files, num_files = '', '', 0
    for k, v in return_dict.items():
        if k == 'num_files':
            num_files = v
        elif k == 'action':
            pass
        elif k == 'sub-action':
            pass
        else:
            hex_val = k
            files = v
    return hex_val, files, num_files


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def del_question(return_dict: dict):

    # ~~~ #             -variables-
    hex_val, files, num_files = dict_hex_finder(return_dict)

    # ~~~ #             -display-
    bp([f'\n{num_files} files share common hex:\n\t{hex_val}', Ct.A], num=0)
    for idx, file in enumerate(files):
        bp([f'\t{idx}', Ct.BBLUE, f': {file}', Ct.GREEN], num=0)

    # ~~~ #             -delete question-
    delete_q = input(f'\nSpecify the file number [0-{num_files - 1}] to '
                     'delete, [S]kip these duplicates, [H]ash the listed '
                     'again, save current state to [J]SON for later deletion, '
                     f'or e[X]it File Deletion: [0-{num_files - 1}/S/H/J/X]: ')
    if delete_q.isdigit():
        d_q = int(delete_q)
        if d_q in range(0, num_files):
            d_ret = del_file(files[d_q])
            if d_ret['success'] == 1:
                return_dict['num_files'] -= 1
                return_dict[hex_val].remove(files[d_q])
                return_dict['action'] = 'del_question'
                return return_dict
        else:
            bp([f'{d_q} out of range [0-{num_files - 1}].', Ct.YELLOW])
            return_dict['action'] = 'del_question'
            return return_dict
    elif delete_q.isalpha():
        if delete_q.lower() == 'x':
            yn_return = yn_question()
            if yn_return == 'y':
                return_dict['sub-action'] = 'exit'
                return_dict['action'] = 'complete'
                return return_dict
            else:
                return_dict['action'] = 'del_question'
                return return_dict
        elif delete_q.lower() == 'j':
            return_dict['action'] = 'json'
            return return_dict
        elif delete_q.lower() == 'h':
            return_dict['action'] = 'hash'
            return_dict['sub-action'] == 're-hash'
            return return_dict
        elif delete_q.lower() == 's':
            return_dict['sub-action'] = 'skip'
            return_dict['action'] = 'complete'
            return return_dict
        else:
            bp([f'{delete_q} invalid option. Try again.', Ct.YELLOW])
            return return_dict
    else:
        bp([f'{delete_q} is neither a digit nor a letter.', Ct.YELLOW])
        return_dict['action'] = 'del_question'
        return return_dict


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def del_logic_controller(hex_dict: dict):

    while hex_dict['action'] != 'complete':
        if hex_dict['num_files'] == 1:
            hex_dict['sub-action'] == 'single'
            hex_dict['action'] = 'complete'
        elif hex_dict['action'] == 'json':
            save_json(hex_dict)
            hex_dict['sub-action'] = 'exit'
            hex_dict['action'] = 'complete'
        elif hex_dict['action'] == 'hash':
            hex_val, files, num_files = dict_hex_finder(hex_dict)
            hash_type = 'sha256' if len(hex_val) == 64 else 'blake2b'
            file_confirm = 0
            for file in files:
                return_hex = hash_check(file, hash_type)
                if return_hex == hex_val:
                    file_confirm += 1
            bp([f'\nConfirmed {file_confirm} file hashes match the list of '
                f'{num_files} files with a common hash.', Ct.GREEN])
            if file_confirm == num_files:
                hex_dict['sub-action'] = 're-hashed'
                hex_dict['action'] = 'del_question'
            else:
                bp(['Skipping this hash match. It will be in the log output,'
                    ' and JSON output if specified.', Ct.YELLOW])
                hex_dict['sub-action'] = 'skip'
                hex_dict['action'] = 'complete'
        elif hex_dict['action'] == 'del_question':
            hex_dict = del_question(hex_dict)

    return hex_dict


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
@perf_timer
def expiramental_file_deletion(del_dict: dict):

    return_dict = del_dict
    for k, v in del_dict.items():
        hex_dict = {k: v}
        hex_dict['num_files'] = len(v)
        hex_dict['action'] = 'del_question'
        hex_dict['sub-action'] = 'start'
        del_q_return = del_logic_controller(hex_dict)
        if del_q_return['sub-action'] == 'exit':
            return del_dict
        elif del_q_return['sub-action'] == 'json':
            return_dict[k] = del_q_return[k]

    return return_dict
