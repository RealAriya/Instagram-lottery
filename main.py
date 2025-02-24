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


@app.route("/login", methods=['GET', 'POST'])
def login():
    
    form = LoginForm()
    if form.validate_on_submit():

        # Finds the user in the database based on the email provided in the form.
        user = Users.query.filter_by(email=form.email.data).first()

        # Verifies the user’s password.
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            flash('You entered successfully!', 'success')
            return redirect(url_for('choose_lottery'))
        else:
            flash('Unsuccessfully !!!, Please check our email and password', 'danger')
    return render_template('auth.html', form=form, is_login=True)



@app.route('/choose_lottery', methods=['GET', 'POST'])
def choose_lottery():
    form = LotteryChoiceForm()

    if form.validate_on_submit():

        chosen_type = form.lottery_type.data
        lottery_type = LotteryType(name=chosen_type)

        try:
            db.session.add(lottery_type)
            db.session.commit()
            flash(f'You have chosen: {chosen_type}', 'success')
            return redirect(url_for('start_lottery', lottery_type=chosen_type))
        
        except Exception as e:
            db.session.rollback()
            flash('There was an Error while choosing lottery type', 'danger') 

    return render_template('choose_lottery.html', form=form)
