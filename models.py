from config import bdd

class User(bdd.Model):
    id = bdd.Column(bdd.Integer, primary_key=True)
    username = bdd.Column(bdd.String(80), unique=True, nullable=False)
    email = bdd.Column(bdd.String(120), unique=True, nullable=False)