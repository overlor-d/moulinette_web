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
        username = request.form['identifiant']
        mdp = request.form['mdp']
        print(f" l'id est {username} et le mdp est : {mdp}")

        if bdd.verif_user(username, mdp):
            session['username'] = username
            return redirect(url_for('home'))
    return render_template("login.html")


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))