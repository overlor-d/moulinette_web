from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import timedelta
from itsdangerous import URLSafeTimedSerializer
import os

app = Flask(__name__)

db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'data', 'app.db')
app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = b'C8mH=A6L;84grws/?6F!'
app.permanent_session_lifetime = timedelta(minutes=30)

bdd = SQLAlchemy(app)
migrate = Migrate(app, bdd)

s_token = URLSafeTimedSerializer(app.config['SECRET_KEY'])

from app import routes
