from app import app
from flask import request, redirect, url_for, render_template

from .UserController import signUp, signIn, checkSessionData, clearSessionData, getPersonalisationValues, setPersonalisationValues, checkSessionPref
from .request import businessArticles, entArticles, get_news_source, healthArticles, publishedArticles, randomArticles, scienceArticles, sportArticles, techArticles, topHeadlines, search, personalisedArticles

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        if checkSessionPref():
            articles = personalisedArticles()
        else:
            articles = publishedArticles()
        return render_template('home.html', articles = articles)

    if request.method == "POST":
        data = request.form.to_dict()
        searchResult = search(data)
        if searchResult!=None:
            return render_template('search.html', articles=searchResult)
        else:
            return render_template('error.html')

@app.route("/sign-in", methods=["GET","POST"])
def signInFunction():
    if request.method == "GET":
       if checkSessionData():
        return redirect(url_for("home"))

    if request.method == "POST":
        response = signIn()
        if response:
            personalisedTopicsValues = getPersonalisationValues()
            if personalisedTopicsValues is False:
                return redirect(url_for("setPreferences"))
            else:
                return redirect(url_for("home"))
        else:
            return render_template('Signin.html', msg="Invalid credentials")
    else:
        return render_template('Signin.html')

@app.route("/sign-up", methods=["GET","POST"])
def signUpFunction():
    if checkSessionData():
        return redirect(url_for("home"))
    
    if request.method == "POST":
        response = signUp()
        if response:
            return redirect(url_for("signInFunction"))
        else:
            return render_template('Signup.html', msg="User already exists, please log in")
    else:
        return render_template('Signup.html')


@app.route("/set-preferences", methods=["GET","POST"])
def setPreferences():
    if checkSessionData():
        if request.method=="GET":
            return render_template("preference.html")
        if request.method=="POST":
            #addPreferencesToDB() 
            setPersonalisationValues()
            return redirect(url_for("home"))
    else:
        return redirect(url_for("signInFunction"))

@app.route("/logout")
def logout():
    if clearSessionData():
        return redirect(url_for("home"))
    else:
        return '<h1>An error occurred</h1>'


@app.route('/headlines')
def headlines():
    headlines = topHeadlines()

    return render_template('articles.html', articles = headlines)

@app.route('/articles')
def articles():
    random = randomArticles()

    return render_template('articles.html', articles = random)

@app.route('/sources')
def sources():
    newsSource = get_news_source()

    return render_template('articles.html', articles = newsSource)

@app.route('/category/business')
def business():
    sources = businessArticles()

    return render_template('articles.html', articles = sources)

@app.route('/category/tech')
def tech():
    sources = techArticles()

    return render_template('articles.html', articles = sources)

@app.route('/category/entertainment')
def entertainment():
    sources = entArticles()

    return render_template('articles.html', articles = sources)

@app.route('/category/science')
def science():
    sources = scienceArticles()

    return render_template('articles.html', articles = sources)

@app.route('/category/sports')
def sports():
    sources = sportArticles()

    return render_template('articles.html', articles = sources)

@app.route('/category/health')
def health():
    sources = healthArticles()

    return render_template('articles.html', articles = sources)