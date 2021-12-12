
import json
from betterprint.betterprint import bp
from betterprint.colortext import Ct
from modules.argsval import file_check


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def save_json(json_dict: dict, json_file: str):
    """Save found duplicates to json. This allows importing later instead of
    rescanning the entire folder structure again.

    - Args:
        - json_dict (dict):
            - k:    the unique hex value
            - v:    each file sharing that unique value
    """
# ~~~ #                     -validation-
    json_output_val = file_check(json_file, action='overwrite')
    try:
        with open(json_output_val, 'w') as jsonf:
            json.dump(json_dict, jsonf, indent=4)
    except OSError as e:
        bp([f'cannot save json file {json_output_val}.\n\t{e}\n', Ct.RED],
            err=2)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def import_json(json_file: str):
    """Import a json file to process previously scanned duplicates.

    - Returns:
        - [dict]:
            - k:    the unique hex value
            - v:    each file sharing that unique value
    """
    try:
        return_dict = {'dupe_dict': {}, 'dupe_files': 0, 'dupe_hashes': 0}
        with open(json_file, 'r') as jsonf:
            json_dict = json.load(jsonf)
        return_dict['dupe_dict'] = json_dict
        # count the duplicate files and hashes
        for k, v in json_dict.items():
            if len(v) > 1:
                return_dict['dupe_files'] += len(v)
                return_dict['dupe_hashes'] += 1
        return return_dict
    except OSError as e:
        bp([f'trying to delete file.\n\t{e}\n', Ct.RED], err=2)
