from fonctions_annexes import *
import os

class Index:
    def __init__(self) -> None:
        self.path = "./data/index.json"


    def load_index(self):
        data_index = load_json_data(self.path)

        if data_index == {}:
            data_index = {
                "email" : {}
            }
            dump_json_data(self.path,data_index)

        return data_index


    def ajout_mail(self, username = None):
        index_data = self.load_index()

        

        if username:
            
            path_dir = f"./data/users/{username}/"
            
            file_path = os.path.join(path_dir, "info.json")

            if os.path.exists(file_path):
                contenu = load_json_data(file_path)
                if contenu["email"] not in index_data["email"]:
                    index_data["email"][contenu["email"]] = contenu["username"]

        else :

            path_dir = "./data/users"

            for dossier in os.listdir(path_dir):
                user_dir = os.path.join(path_dir, dossier)

                if os.path.isdir(user_dir):
                    info_file = os.path.join(user_dir, "info.json")

                    if os.path.exists(info_file):
                        
                        contenu = load_json_data(info_file)
                        
                        if contenu["email"] not in index_data["email"]:
                            index_data["email"][contenu["email"]] = contenu["username"]

        dump_json_data("./data/index.json",index_data)
        return 1


class Data:
    def __init__(self):
        self.index = Index()


    def load_user(self,username_email):
        if conform_mail(username_email):
            username = self.search_username_by_mail(username_email)
            if username == None:
                return None
        else :
            username = username_email
        path_user = f"./data/users/{username}/info.json"


        if self.user_exist(username):
            return load_json_data(path_user)
        else :
            return None


    def update_user(self,new_data):
        if dump_json_data(new_data) != 0:
            print("Problème lors de la mise à jour des données du user")
            return 1
        else :
            return 0
    

    def create_user(self, username, mdp, email) -> int:
        path_file = f"./data/users/{username}/info.json"
        if self.user_exist(username):
            print("Le user existe déjà")
            return 1
        
        with open(path_file, "w") as file:
            pass

        new_user = {
            "email" : email,
            "username" : username,
            "password" : mdp
        }


        if dump_json_data(path_file, new_user) == 1:
            print("Erreur lors de la création du user")
            return 1

        self.index.ajout_mail(username)

        return 0


    def del_user(self, username_email) -> int:
        pass


    def user_exist(self, username) -> bool:
        return os.path.exists(f"./data/users/{username}.json")


    def verif_user(self,username_email, mdp):
        user = self.load_user(username_email)

        if user != None and user["password"] == mdp:
            return True
        return False


    def search_username_by_mail(self, mail):
        index = self.index.load_index()
        return index.get("email", {}).get(mail, None)


if __name__ == "__main__":
    dat = Data()

    dat.maj_index_mail()