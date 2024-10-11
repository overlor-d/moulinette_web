import json

def load_json_data(path_file):
    try :
        with open(path_file, 'r') as file:
            json_content = json.load(path_file)
        return json_content
    except :
        return None

def dump_json_data(path_file, data):
    try :
        with open(path_file, 'w') as file:
            json.dump(data, file)
        return 0
    except:
        return 1