import json
import re
import os
import shutil


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


