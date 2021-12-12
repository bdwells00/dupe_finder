
import os
from betterprint.betterprint import bp
from betterprint.colortext import Ct
from modules.argsval import yn_question
from modules.filechecks import hash_check
from modules.jsonfinder import save_json
from modules.timer import perf_timer


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def del_file(file: str):
    """Delete file.

    - Args:
        - file (str): file to delete

    - Returns:
        - [dict]: dict to track successful deletions
            - 'file': the file to delete
            - 'success': 0 = no, 1 = yes
    """
    # ~~~ #                 -variables-
    return_dict = {'file': file, 'success': 0}

    # ~~~ #                 -delete-
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
def dict_hex_finder(single_hex_dict: dict):
    """Pulls the 'hex' key, 'num_files' key, and the file list out of the dict.

    - Args:
        - single_hex_dict (dict): dict with one hex, plus various other keys

    - Returns:
        - 0 [str]: hex
        - 1 [list]: files
        - 2 [int]: number of files
    """
    hex_val, files, num_files = '', '', 0
    for k, v in single_hex_dict.items():
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
def del_question(single_hex_dict: dict):
    """Interactive input section asking which file to delete, or take other
    action.

    - Args:
        - single_hex_dict (dict): dict with one hex, plus various other keys

    - Returns:
        - single_hex_dict [dict]: after processing and/or updating
    """
    # ~~~ #                 -variables-
    hex_val, files, num_files = dict_hex_finder(single_hex_dict)

    # ~~~ #                 -display-
    bp([f'\n{num_files} files share common hex:\n\t{hex_val}', Ct.A], num=0)
    for idx, file in enumerate(files):
        bp([f'\t{idx}', Ct.BBLUE, f': {file}', Ct.GREEN], num=0)

    # ~~~ #                 -delete question-
    delete_q = input(f'\nSpecify the file number [0-{num_files - 1}] to '
                     'delete, [S]kip these duplicates, [H]ash the listed '
                     'again, save current state to [J]SON for later deletion, '
                     f'or e[X]it File Deletion: [0-{num_files - 1}/S/H/J/X]: ')
    # check if string is a number
    if delete_q.isdigit():
        # set new var to an int version for comparison
        d_q = int(delete_q)
        # check if the digit is within the range of files to delete
        if d_q in range(0, num_files):
            # call the delete file function  ***This is the delete part***
            deletion_return_dict = del_file(files[d_q])
            # if the delete was successful, update and return the dict
            if deletion_return_dict['success'] == 1:
                single_hex_dict['num_files'] -= 1
                single_hex_dict[hex_val].remove(files[d_q])
                single_hex_dict['action'] = 'del_question'
                return single_hex_dict
            # set sub-action to failure and return
            else:
                single_hex_dict['sub-action'] = 'failure'
                single_hex_dict['action'] = 'complete'
                return single_hex_dict
        # number not in range, re-ask question
        else:
            bp([f'{d_q} out of range [0-{num_files - 1}].', Ct.RED])
            single_hex_dict['action'] = 'del_question'
            return single_hex_dict
    # check if string is a letter
    elif delete_q.isalpha():
        # x for exit
        if delete_q.lower() == 'x':
            # confirm exit request was not accidental
            yn_return = yn_question()
            # exit if yes
            if yn_return == 'y':
                single_hex_dict['sub-action'] = 'exit'
                single_hex_dict['action'] = 'complete'
                return single_hex_dict
            # re-ask del question if it was accidental
            else:
                single_hex_dict['action'] = 'del_question'
                return single_hex_dict
        # set action to json to save and then exit
        elif delete_q.lower() == 'j':
            single_hex_dict['action'] = 'json'
            return single_hex_dict
        # set action to hash, then return for rehashing
        elif delete_q.lower() == 'h':
            single_hex_dict['action'] = 'hash'
            single_hex_dict['sub-action'] == 're-hash'
            return single_hex_dict
        # skip this hex; it will be saved as is
        elif delete_q.lower() == 's':
            single_hex_dict['sub-action'] = 'skip'
            single_hex_dict['action'] = 'complete'
            return single_hex_dict
        # is not one of the available options, re-ask
        else:
            bp([f'{delete_q} invalid option. Try again.', Ct.YELLOW])
            return single_hex_dict
    # invalid choice
    else:
        bp([f'{delete_q} is neither a digit nor a letter.', Ct.YELLOW])
        single_hex_dict['action'] = 'del_question'
        return single_hex_dict


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def del_logic_controller(single_hex_dict: dict):
    """While loop allowing multiple files sharing a single hex to be deleted
    until down to a single file.

    - Args:
        - single_hex_dict (dict): dict with one hex, plus various other keys

    - Returns:
        - single_hex_dict [dict]: after processing and/or updating
    """
    # while loop keep the questions going until 'action' is set to 'complete'
    while single_hex_dict['action'] != 'complete':
        # if num_files left is one, set action to complete breaking the loop
        if single_hex_dict['num_files'] == 1:
            single_hex_dict['sub-action'] == 'single'
            single_hex_dict['action'] = 'complete'
        # if 'json', save to json, set to complete to break
        elif single_hex_dict['action'] == 'json':
            save_json(single_hex_dict)
            single_hex_dict['sub-action'] = 'json'
            single_hex_dict['action'] = 'complete'
        # if 'hash', re-hash
        elif single_hex_dict['action'] == 'hash':
            hex_val, files, num_files = dict_hex_finder(single_hex_dict)
            hash_type = 'sha256' if len(hex_val) == 64 else 'blake2b'
            file_confirm = 0
            for file in files:
                return_hex = hash_check(file, hash_type)
                if return_hex == hex_val:
                    file_confirm += 1
            bp([f'\nConfirmed {file_confirm} file hashes match the list of '
                f'{num_files} files with a common hash.', Ct.GREEN])
            # relaunch del_question by setting 'action' for while loop
            if file_confirm == num_files:
                single_hex_dict['sub-action'] = 're-hashed'
                single_hex_dict['action'] = 'del_question'
            # set to 'hash-mismatch' and skip this hex
            else:
                bp(['Skipping this hash match. It will be in the log output,'
                    ' and JSON output if specified.', Ct.YELLOW])
                single_hex_dict['sub-action'] = 'hash-mismatch'
                single_hex_dict['action'] = 'complete'
        # launch del_question
        elif single_hex_dict['action'] == 'del_question':
            single_hex_dict = del_question(single_hex_dict)

    return single_hex_dict


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
@perf_timer
def expiramental_file_deletion(dedupe_dict: dict):
    """Entry function that iterates through each hex key, sending it off to
    process for deletion.

    - Args:
        - dedupe_dict (dict): full dict of all hexes (keys) and files (values)

    - Returns:
        - [dict]: an updated dict with the remaining keys and values
    """
    # copy of the dict to return
    return_dict = dedupe_dict
    # iterate through each hex with multiple files
    for k, v in dedupe_dict.items():
        # new single hex dict to send off for processing
        single_hex_dict = {k: v}
        # add additional 3 keys to allow processing options and passing only
        # this single dict around between functions
        single_hex_dict['num_files'] = len(v)
        single_hex_dict['action'] = 'del_question'
        single_hex_dict['sub-action'] = 'start'
        del_q_return = del_logic_controller(single_hex_dict)
        # if the hash hash still has multiple properties
        if del_q_return['num_files'] > 1:
            # exit the delete section and finish the program
            if del_q_return['sub-action'] == 'exit':
                return dedupe_dict
            # update the return dict in case of changes and exit
            elif del_q_return['sub-action'] == 'json':
                return_dict[k] = del_q_return[k]
                return return_dict
            # update the return dict in case of changes and exit
            elif del_q_return['sub-action'] == 'skip':
                return_dict[k] = del_q_return[k]
            # TODO figure out what to do with failures
            elif del_q_return['sub-action'] == 'failure':
                # TODO exit immediately? save to json? skip? ask customer?
                pass
            # TODO figure out what to do with hash mismatches
            elif del_q_return['sub-action'] == 'hash-mismatch':
                # TODO exit immediately? save to json? skip? ask customer?
                pass
        # else the hash must be down to one and can be removed from return_dict
        else:
            # protect from crash and exit if can't pop
            try:
                return_dict.pop(k)
            except KeyError as e:
                bp([f'could not remove {k} from the dictionary of duplicate '
                    f'files.\n{e}\nContinuing, but if error recurs, choose '
                    'exit and troubleshoot issue.', Ct.RED], erl=2)
                continue

    return return_dict
