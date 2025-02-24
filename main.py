from flask import Flask, render_template, redirect, url_for, request, flash
from models import db, bcrypt, Users, LotteryType
import os



# Connect to lottery database
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/lottery"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY', 'your_default_secret_key')


# Initialize extensions
db.init_app(app)
bcrypt.init_app(app)


# Create database tables
with app.app_context():
    db.create_all()


# Routes
@app.route('/')
def index():
    return render_template("index.html")