import json

def dump_json(path_file):
    with open(path_file, 'r') as file:
        json_content = json.load(path_file)

    return json_content