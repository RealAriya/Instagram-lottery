from flask import Flask, render_template, redirect, url_for, request, flash
from models import db, bcrypt, Users, LotteryType
from forms import RegistrationForm, LoginForm, LotteryChoiceForm
from data_scraper import login, collect_comments, collect_likes, collect_followers
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import random
from payment import process_payment
from excel_generator import generate_excel



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



@app.route('/start_lottery/<lottery_type>', methods=['GET', 'POST'])
def start_lottery(lottery_type):
    form = LotteryChoiceForm()
    if form.validate_on_submit():
        post_url = request.form['post_url']
        min_comments = form.min_comments.data
        min_mentions = form.min_mentions.data

        # Initialize ChromeDriver
        service = Service('/usr/bin/chromedriver')  
        driver = webdriver.Chrome(service=service)
        login(driver)

        participants = []
        if 'comments' in lottery_type:
            comments = collect_comments(driver, post_url)
            filtered_comments = {
                user: data for user, data in comments.items()
                if data['comment_count'] >= min_comments and data['mention_count'] >= min_mentions
            }
            participants.extend(list(filtered_comments.keys()))
        if 'likes' in lottery_type:
            likes = collect_likes(driver, post_url)
            participants.extend(likes)
        if 'followers' in lottery_type:
            followers = collect_followers(driver, post_url)
            participants.extend(followers)

        driver.quit()

        # Check if payment is required
        if len(participants) >= 100:  
            payment_url = process_payment(amount=1000, callback_url=url_for('lottery_result', _external=True))
            if payment_url:
                return redirect(payment_url)
            else:
                flash('Payment processing failed. Please try again.', 'danger')
                return redirect(url_for('start_lottery', lottery_type=lottery_type))

        # Save the participant data to an Excel file:
        generate_excel({"username": participants}, 'participants.xlsx')

        # Select a winner
        winner = random.choice(participants)
        return redirect(url_for('lottery_result', winner=winner))

    return render_template('lottery.html', form=form, lottery_type=lottery_type)


