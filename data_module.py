import os
from werkzeug.security import check_password_hash
from fonctions_annexes import *

class Index:
    def __init__(self):
        self.path = "./data/index.json"

    def load_index(self):
        data_index = load_json_data(self.path)
        if not data_index:
            data_index = {"email": {}}
            dump_json_data(self.path, data_index)
        return data_index

    def ajout_mail(self, username=None):
        index_data = self.load_index()
        path_dir = f"./data/users/{username}/" if username else "./data/users/"

        if username:
            info_file = os.path.join(path_dir, "info.json")
            if os.path.exists(info_file):
                contenu = load_json_data(info_file)
                if contenu["email"] not in index_data["email"]:
                    index_data["email"][contenu["email"]] = contenu["username"]
        else:
            for dossier in os.listdir(path_dir):
                user_dir = os.path.join(path_dir, dossier)
                if os.path.isdir(user_dir):
                    info_file = os.path.join(user_dir, "info.json")
                    if os.path.exists(info_file):
                        contenu = load_json_data(info_file)
                        if contenu["email"] not in index_data["email"]:
                            index_data["email"][contenu["email"]] = contenu["username"]

        dump_json_data(self.path, index_data)
        return 1


class Data:
    def __init__(self):
        self.index = Index()

    def load_user(self, username_email):
        if conform_mail(username_email):
            username = self.search_username_by_mail(username_email)
            if not username:
                return None
        else:
            username = username_email

        path_user = f"./data/users/{username}/info.json"
        if self.user_exist(username):
            return load_json_data(path_user)
        return None

    def create_user(self, username, password, email):
        user_dir = f"./data/users/{username}/"
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)

        user_data = {
            "email": email,
            "username": username,
            "password": password
        }

        info_file = os.path.join(user_dir, "info.json")
        dump_json_data(info_file, user_data)

        self.index.ajout_mail(username)

    def user_exist(self, username):
        return os.path.exists(f"./data/users/{username}")

    def verif_user(self, username_email, mdp):
        user = self.load_user(username_email)
        if user and check_password_hash(user['password'], mdp):
            return True
        return False

    def search_username_by_mail(self, mail):
        index = self.index.load_index()
        return index.get("email", {}).get(mail, None)
