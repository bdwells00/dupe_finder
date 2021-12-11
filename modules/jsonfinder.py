
import json
from betterprint.betterprint import bp
from betterprint.colortext import Ct
from modules.options import args


def save_json(json_dict: dict):

    try:
        with open(args.json_output, 'w') as jsonf:
            json.dump(json_dict, jsonf, indent=4)
    except OSError as e:
        bp([f'trying to delete file.\n\t{e}\n', Ct.RED], err=2)


def import_json():

    try:
        return_dict = {'dupe_dict': {}, 'dupe_files': 0, 'dupe_hashes': 0}
        with open(args.json_input, 'r') as jsonf:
            json_dict = json.load(jsonf)
        return_dict['dupe_dict'] = json_dict
        for k, v in json_dict.items():
            if len(v) > 1:
                return_dict['dupe_files'] += len(v)
                return_dict['dupe_hashes'] += 1
        return return_dict
    except OSError as e:
        bp([f'trying to delete file.\n\t{e}\n', Ct.RED], err=2)
