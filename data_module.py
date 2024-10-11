from fonctions_annexes import *
import os

class Data:
    def __init__(self):
        pass


    def load_user(self,username):
        path_user = f"./data/users/{username}.json"

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
    

    def create_user(self, username, mdp) -> int:
        path_file = f"./data/users/{username}.json"
        if self.user_exist(username):
            print("Le user existe déjà")
            return 1
        
        with open(path_file, "w") as file:
            pass

        new_user = {
            "username" : username,
            "password" : mdp
        }

        if dump_json_data(path_file, new_user) == 1:
            print("Erreur lors de la création du user")
            return 1
        return 0


    def del_user(self, username) -> int:
        pass


    def user_exist(self, username) -> bool:
        return os.path.exists(f"./data/users/{username}.json")


    def verif_user(self,username, mdp):
        user = self.load_user(username)

        if user["password"] == mdp:
            return True
        return False

if __name__ == "__main__":
    dat = Data()

    dat.create_user("over", "mdpdd")

    user = dat.load_user("over")
    
    print(dat.verif_user("over","mdpdd"))