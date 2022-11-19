from app import app
from flask import Flask
from flask_mail import Mail, Message
from .config import SendGridMailConfig

mail = Mail(app)

app.config['MAIL_SERVER']= SendGridMailConfig.MAIL_SERVER
app.config['MAIL_PORT'] = SendGridMailConfig.MAIL_PORT
app.config['MAIL_USERNAME'] = SendGridMailConfig.MAIL_DEFAULT_SENDER
app.config['MAIL_PASSWORD'] = SendGridMailConfig.MAIL_PASSWORD
app.config['MAIL_DEFAULT_SENDER'] = SendGridMailConfig.MAIL_DEFAULT_SENDER
app.config['SECURITY_EMAIL_SENDER'] = SendGridMailConfig.MAIL_DEFAULT_SENDER
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

def sendWelcomeMail(userMail):
    recipientList = [userMail]
    msg = Message(
        'Hello',
        sender=SendGridMailConfig.MAIL_DEFAULT_SENDER,
        recipients=recipientList
    )
    msg.body = 'Thank you for creating a NewsTracker account. Hope you have a pleasant experience going ahead'
    mail.send(msg)
    