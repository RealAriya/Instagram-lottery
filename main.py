from flask import Flask, render_template, redirect, url_for, request, flash
from models import db, bcrypt, Users, LotteryType
from forms import RegistrationForm, LoginForm, LotteryChoiceForm
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


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user = Users(username=form.username.data, email=form.email.data, password=hashed_password)

        try:
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created! , Now you can enter', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('There was an Error while creating your account !!!', 'danger')
    return render_template('auth.html', form=form, is_login=False)