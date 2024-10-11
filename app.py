from flask import Flask, render_template, request
from flask import url_for

app = Flask(__name__)

@app.route('/')
def index():
    return 'index'

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifiant = request.form['identifiant']
        mdp = request.form['mdp']
        print(f" l'id est {identifiant} et le mdp est : {mdp}")
    return render_template('login.html')

