import ibm_db
from flask import request, session
from .mail import sendWelcomeMail

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
        setSessionEmail(data["email"])
        setSessionPref()
        return True
    else:
        return False

def signUp():
    data = request.form.to_dict()
    sendWelcomeMail(data["email"])
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
    
    return True

def checkSessionData():
    if 'email' in session:
        return True
    else:
        return False

def checkSessionPref():
    if 'preference-set' in session:
        return session['preference-set']==True
    else:
        return False

def setSessionEmail(email):
    session['email'] = email
    return True

def setSessionPref():
    session['preference-set'] = False
    get_user_preferences = "SELECT PREFERENCE_1 FROM PREFERENCES WHERE EMAIL = '{}'".format(session['email'])
    check_get_user_preferences = ibm_db.exec_immediate(DB.DB_URI, get_user_preferences)
    try:
        value = ibm_db.fetch_tuple(check_get_user_preferences)
        if value!=False:
            print(value)
            session['preference-set'] = True
        return value
    except Exception as e:
        print(e)

def clearSessionData():
    if session.pop('email', None):
        session.pop('preference-set', None)
        return True
    else:
        return False


def getPersonalisationValues():
    email = session['email']
    get_user_preferences = "SELECT PREFERENCE_1, PREFERENCE_2, PREFERENCE_3, PREFERENCE_4, PREFERENCE_5 FROM PREFERENCES WHERE EMAIL = '{}'".format(email)
    check_get_user_preferences = ibm_db.exec_immediate(DB.DB_URI, get_user_preferences)
    try:
        value = ibm_db.fetch_tuple(check_get_user_preferences)
        return value
    except Exception as e:
        print(e)
        
def setPersonalisationValues():
    email = session['email']
    data = request.form.to_dict()
    sql_query = "INSERT INTO PREFERENCES (EMAIL, PREFERENCE_1, PREFERENCE_2, PREFERENCE_3, PREFERENCE_4, PREFERENCE_5) VALUES('{}','{}','{}','{}','{}','{}')".format(email, data['Preference_1'], data['Preference_2'], data['Preference_3'], data['Preference_4'], data['Preference_5'])
    sql_query_response = ibm_db.exec_immediate(DB.DB_URI, sql_query)
    try:
        value = ibm_db.fetch_tuple(sql_query_response)
    except Exception as e:
        print(e)
        return False
    return True

"""def sendVerificationMail(receiverEmail):
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