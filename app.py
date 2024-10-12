from flask import Flask, render_template, request, session, redirect
from flask import url_for
from data_module import *
from datetime import timedelta

app = Flask(__name__)
bdd = Data()

app.permanent_session_lifetime = timedelta(minutes=30)
app.secret_key = b'C8mH=A6L;84grws/?6F!'


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


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_mail = request.form['username_mail']
        mdp = request.form['mdp']

        if bdd.verif_user(username_mail, mdp):
            session['username'] = username_mail
            return redirect(url_for('home'))
        else :
            if conform_mail(username_mail):
                message_error = "Mail ou mot de passe incorrect"
            else:
                message_error = "Username ou mot de passe incorrect"

            return render_template('login.html', error=message_error)
        
    if 'username' in session:
        return redirect(url_for("home"))
    return render_template("login.html")


@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["mdp"]
        confirm_passwd = request.form["confirm_mdp"]

        if password != confirm_passwd:
            error_mdp = "Les deux mots de passes ne correspondent pas"
            return render_template("register.html", error_mdp = error_mdp)
        
        if check_password_policy(password):
            error_mdp = "Le password ne convient pas à la politique imposée : 12 caractères, un caractère spécial minimum et un chiffre minimum"
            return render_template("register.html", error_mdp = error_mdp)
        
        if len(username) < 3:
            error_username = "Le username est trop petit il doit comporter au moins 3 caractères"
            return render_template("register.html", error_username = error_username)
        
        if not conform_mail(email):
            error_email = "Le mail spécifié n'est pas conforme"
            return render_template("register.html", error_email = error_email)
        
        if bdd.search_username_by_mail(email) != None:
            error_email = "Le mail spécifié est déjà utilisé"
            return render_template("register.html", error_email = error_email)

        if bdd.user_exist(username):
            error_username = "Le username est déjà utilisé par quelqu'un d'autre"
            return render_template("register.html", error_username = error_username)



        bdd.create_user(username, password, email)
        return redirect(url_for("home"))

    return render_template("register.html")


@app.route('/recovery', methods = ['GET', 'POST'])
def recovery():
    return render_template("recovery.html")

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))