from flask import render_template, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from fonctions_annexes import *
from config import app, bdd
from models import User


@app.route('/home')
def home():
    if 'username' in session:
        return render_template("connect.html")
    return redirect(url_for('login'))


@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_mail = request.form['username_mail']
        mdp = request.form['mdp']

        user = bdd.load_user(username_mail)
        if user and check_password_hash(user['password'], mdp):
            session['username'] = user['username']
            return redirect(url_for('home'))
        else:
            error = "Email ou mot de passe incorrect"
            return render_template('login.html', error=error)
        
    if 'username' in session:
        return redirect(url_for('home'))
    return render_template("login.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["mdp"]
        confirm_passwd = request.form["confirm_mdp"]

        if password != confirm_passwd:
            return render_template("register.html", error_mdp="Les mots de passe ne correspondent pas")
        
        if not check_password_policy(password):
            return render_template("register.html", error_mdp="Le mot de passe ne respecte pas la politique")

        if len(username) < 3:
            return render_template("register.html", error_username="Le nom d'utilisateur est trop court")

        if not conform_mail(email):
            return render_template("register.html", error_email="Le mail n'est pas conforme")

        if bdd.search_username_by_mail(email):
            return render_template("register.html", error_email="Le mail est déjà utilisé")

        if bdd.user_exist(username):
            return render_template("register.html", error_username="Le nom d'utilisateur est déjà utilisé")

        hashed_password = generate_password_hash(password)

        bdd.create_user(username, hashed_password, email)
        return redirect(url_for('login'))

    return render_template("register.html")


@app.route('/recovery', methods=['GET', 'POST'])
def recovery():
    return render_template("recovery.html")


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))
