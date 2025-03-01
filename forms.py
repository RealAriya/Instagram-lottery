from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField , SelectField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length


# Sign up
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=12)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, message="Password must be at least 8 characters long.")])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message="Passwords must match.")])
    submit = SubmitField('Sign up')

# Log in
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


# Lottery choise
# Allows users to select a lottery type.

class LotteryChoiceForm(FlaskForm):
    lottery_type = SelectField('Select Lottery Type', choices=[
        ('comments', 'Lottery by Comments'),
        ('likes', 'Lottery by Likes'),
        ('score', 'Lottery by Score'),
        ('followers', 'Lottery by Followers')
    ],validators=[DataRequired()])
    
    submit = SubmitField('Proceed')


class StartLotteryForm(FlaskForm):
    post_url = StringField('Instagram Post URL', validators=[DataRequired()])
    min_comments = IntegerField('Minimum Comments', default=0, validators=[DataRequired()])
    min_mentions = IntegerField('Minimum Mentions', default=0, validators=[DataRequired()])
    submit = SubmitField('Run Lottery')