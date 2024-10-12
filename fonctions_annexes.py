import json
import re
import os
import shutil

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
    

def conform_mail(mail):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    
    if re.match(email_regex, mail):
        return True
    else:
        return False


def check_password_policy(password):
    if len(password) < 12 or not re.search(r'\d', password) or not re.search(r'\W', password):
        return False
    return True


def duplicate_folder(src, dest):

    if not os.path.exists(src):
        return 1
    
    if os.path.exists(dest):
        return 2
    
    shutil.copytree(src, dest)
    