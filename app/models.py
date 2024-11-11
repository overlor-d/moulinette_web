from app import bdd
from datetime import datetime, timezone

class User(bdd.Model):
    id = bdd.Column(bdd.Integer, primary_key=True, unique=True)
    username = bdd.Column(bdd.String(80), unique=True, nullable=False)
    email = bdd.Column(bdd.String(120), unique=True, nullable=False)
    password_hash = bdd.Column(bdd.String(120), nullable=False)
    created_at = bdd.Column(bdd.DateTime, defaut=datetime.now(timezone.utc))
    role = bdd.Column(bdd.String(100), nullable = False)
    

class Password(bdd.Model):
    id = bdd.Column(bdd.Integer, primary_key=True, unique=True)
    hash_mdp = bdd.Column(bdd.String(120))
    