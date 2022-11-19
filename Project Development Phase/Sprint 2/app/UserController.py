import ibm_db
from flask import request, session
""" from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail """

from .config import DB

def signIn():
    data = request.form.to_dict()
    check_user_exists = "SELECT email from USERS WHERE email = '{}'".format(data["email"])
    check_user_exists_response = ibm_db.exec_immediate(DB.DB_URI, check_user_exists)
    try:
        value = ibm_db.fetch_tuple(check_user_exists_response)[0].replace(" ","")
        pass
    except:
        print('User does not exist')
        return False
    sql_query = "SELECT userPassword FROM USERS WHERE email = '{}'".format(data["email"])
    result = ibm_db.exec_immediate(DB.DB_URI,sql_query)
    value = ibm_db.fetch_tuple(result)[0].replace(" ","")

    if value == data["password"]:
        setSessionData(data["email"])
        return True
    else:
        return False

def signUp():
    data = request.form.to_dict()
    existing_user_sql_query = "SELECT email FROM USERS WHERE EMAIL ='{}'".format(data["email"])
    existing_user_response = ibm_db.exec_immediate(DB.DB_URI, existing_user_sql_query)
    try:
        value = ibm_db.fetch_tuple(existing_user_response)[0].replace(" ","")
        if value is not None:
            print('User already exists')
            return False
    except:
        pass
    sql_query = "INSERT INTO USERS (email, username, userPassword) VALUES('{}','{}','{}')".format(data["email"], data["username"], data["password"])
    ibm_db.exec_immediate(DB.DB_URI, sql_query)
    """ sendVerificationMail(data["email"]) """
    return True

def checkSessionData():
    if 'email' in session:
        return True
    else:
        return False

def setSessionData(email):
    session['email'] = email
    return True

def clearSessionData():
    if session.pop('email', None):
        return True
    else:
        return False

""" def sendVerificationMail(receiverEmail):
    message = Mail(
        from_email = SendGridMailConfig.MAIL_DEFAULT_SENDER,
        to_emails = receiverEmail,
        subject = 'Verification mail for News Tracker Application',
        html_content = '<p><a href="localhost:5000/verify-email">Click here</a> to verify your email<p>',
    )

    try:
        sendMail = SendGridAPIClient(SendGridMailConfig.MAIL_PASSWORD)
        response = sendMail.send(message)
        print(response)
    except Exception as e:
        print(e.message) """