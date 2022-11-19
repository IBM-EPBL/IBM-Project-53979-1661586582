from app import app
from flask import request, redirect, url_for, render_template

from .UserController import signUp, signIn, checkSessionData, clearSessionData
from .request import businessArticles, entArticles, get_news_source, healthArticles, publishedArticles, randomArticles, scienceArticles, sportArticles, techArticles, topHeadlines

@app.route('/')
def home():
    if checkSessionData():
        articles = publishedArticles()

        return render_template('home.html', articles = articles)
    else:
        return render_template('home.html')


@app.route("/sign-in", methods=["GET","POST"])
def signInFunction():
    if checkSessionData():
        return redirect(url_for("home"))

    if request.method == "POST":
        response = signIn()
        if response:
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

@app.route("/logout")
def logout():
    if clearSessionData():
        return redirect(url_for("home"))
    else:
        return '<h1>An error occurred</h1>'


@app.route('/headlines')
def headlines():
    return render_template('articles.html')

@app.route('/articles')
def articles():
    return render_template('articles.html')

@app.route('/sources')
def sources():
    return render_template('articles.html')

@app.route('/category/business')
def business():
    return render_template('articles.html')

@app.route('/category/tech')
def tech():
    return render_template('articles.html')

@app.route('/category/entertainment')
def entertainment():
    return render_template('articles.html')

@app.route('/category/science')
def science():
    return render_template('articles.html')

@app.route('/category/sports')
def sports():
    return render_template('articles.html')

@app.route('/category/health')
def health():
    return render_template('articles.html')