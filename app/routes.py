from flask import render_template, request, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, bdd, s_token
from itsdangerous import SignatureExpired, BadSignature
from app.fonctions_annexes import *
from app.models import User


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

        user = User.query.filter((User.username == username_mail) | (User.email == username_mail)).first()
        if user and check_password_hash(user.password_hash, mdp):
            session['username'] = user.username
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
            return render_template("register.html", error_confirm_mdp="Les mots de passe ne correspondent pas")
        
        if not check_password_policy(password):
            return render_template("register.html", error_mdp="Le mot de passe ne respecte pas la politique")

        if len(username) < 3:
            return render_template("register.html", error_username="Le nom d'utilisateur est trop court")

        if not conform_mail(email):
            return render_template("register.html", error_email="Le mail n'est pas conforme")

        if User.query.filter_by(email=email).first():
            return render_template("register.html", error_email="Le mail ou le nom d'utilisateur est déjà pris.")

        if User.query.filter_by(username=username).first():
            return render_template("register.html", error_email="Le mail ou le nom d'utilisateur est déjà pris.")

        hashed_password = generate_password_hash(password)

        new_user = User(username=username, email=email, password_hash=hashed_password, permission="user")

        bdd.session.add(new_user)
        try:
            bdd.session.commit()
        except Exception as e:
            bdd.session.rollback()
            flash("Une erreur est survenue lors de l'inscription, veuillez réessayer ou contacter le support.")
            return render_template("register.html")

        return redirect(url_for('login'))

    if 'username' in session:
        return redirect(url_for('home'))

    return render_template("register.html")


@app.route('/recovery', methods=['GET', 'POST'])
def recovery():
    if request.method == "POST":
        email = request.form["email"]
        if User.query.filter_by(email=email).first():
            token = s_token.dumps(email, salt='password-reset-salt')

            link = url_for('reset_password', token=token, _external=True)

            send_email(User.query.filter_by(email=email).first().email, "Réinitialisation de mot de passe", f"Une demande de réinitialisation de mot de passe a été faite. Cliquez sur ce lien pour réinitialiser celui-ci : {link}")

            return redirect(url_for('succes_submit'))

        return redirect(url_for('succes_submit'))

    return render_template("recovery.html")


@app.route('/recovery/submit')
def succes_submit():
    return render_template("recovery/succes.html")


@app.route('/recovery/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = s_token.loads(token, salt='password-reset-salt', max_age=3600)
    except SignatureExpired or BadSignature as e:
        return render_template("/recovery/token_issues.html")
    
    if request.method == "POST":

        password = request.form["password"]
        confirm_passwd = request.form["confirm_paswd"]

        if password != confirm_passwd:
            return render_template("/recovery/resetPassword.html", error_confirm_mdp="Les mots de passe ne correspondent pas", token=token)
    
        if not check_password_policy(password):
            return render_template("/recovery/resetPassword.html", error_new_mdp="Le mot de passe ne respecte pas la politique", token=token)
    
        user = User.query.filter_by(email=email).first()

        user.password_hash = generate_password_hash(password)
        bdd.session.commit()
        print("password réinitialisé")
        return redirect(url_for('login'))


    return render_template("recovery/resetPassword.html", token=token)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))
