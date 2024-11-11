import re

# email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


MAIL_BOT = "moulinetteverif@gmail.com"
MDP_APP_BOT = "erob kyoc chya ainz"


def conform_mail(mail):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    
    if re.match(email_regex, mail):
        return True
    else:
        return False


def check_password_policy(password):
    if len(password) < 12 or not re.search(r'\d', password) or not re.search(r'\W', password):
        return False
    return True


def send_email(adresse_destinataire, sujet, corps):
    email = MIMEMultipart()
    email['From'] = MAIL_BOT
    email['To'] = adresse_destinataire
    email['Subject'] = sujet
    email.attach(MIMEText(corps, 'plain'))

    serveur = smtplib.SMTP('smtp.gmail.com', 587)
    serveur.starttls()
    serveur.login(MAIL_BOT, MDP_APP_BOT)
    
    serveur.send_message(email)
    serveur.quit()
