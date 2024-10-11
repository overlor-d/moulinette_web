import json

def load_json_data(path_file):
    with open(path_file, 'r') as file:
        json_content = json.load(file)
    return json_content


def dump_json_data(path_file, data):
    try :
        with open(path_file, 'w') as file:
            json.dump(data, file)
        return 
    except:
        return 1