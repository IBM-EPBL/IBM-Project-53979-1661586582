from flask import Flask
from .config import App

app = Flask(__name__)
app.secret_key = App.SECRET_KEY


from app import views