from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField , SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length


# Handles user registration.
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=12)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confrim_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')