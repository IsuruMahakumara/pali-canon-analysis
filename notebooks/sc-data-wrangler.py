import json
from pathlib import Path





def read_json_to_dict(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_dict_to_json(data, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)



def build_sn_index_tree(sn_data):

    pass


def build_an_index_tree(an_data):
    pass



def build_dn_index_tree(dn_data):
    pass



def build_abhidhamma_index_tree(abhidhamma_data):
    pass

