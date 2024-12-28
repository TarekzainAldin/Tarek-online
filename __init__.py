from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Tarek-online.db"
db=SQLAlchemy(app)

from myshop.admin import routes

