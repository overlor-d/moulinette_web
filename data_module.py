from fonctions_annexes import *
import os

class Data:
    
    def __init__():
        pass

    def load_user(self,pseudo):
        path_user = f"{pseudo}.json"
        if os.path.exists(path_user):
            return load_json_data(path_user)
        else :
            return None
        
    def update_user(self,new_data):
        if dump_json_data(new_data) != 0:
            print("Problème lors de la mise à jour des données du user")
            return 1
        else :
            return 0
        