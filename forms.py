from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField , SelectField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional


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
    min_comments = IntegerField('Minimum Comments', default=0, validators=[Optional()])  
    min_mentions = IntegerField('Minimum Mentions', default=0, validators=[Optional()])  
    min_score = IntegerField('Minimum Score', default=5, validators=[Optional()])  
    submit = SubmitField('Run Lottery')

    def validate(self, **kwargs):
        
        if not super().validate(**kwargs):
            return False

        # Get lottery type 
        from flask import request
        lottery_type = request.view_args.get('lottery_type')

        # Conditional 
        if lottery_type in ['comments', 'score']:
            if not self.min_comments.data or self.min_comments.data < 0:
                self.min_comments.errors.append("Minimum comments required for this lottery type")
                return False
            if not self.min_mentions.data or self.min_mentions.data < 0:
                self.min_mentions.errors.append("Minimum mentions required for this lottery type")
                return False
            if lottery_type == 'score' and (not self.min_score.data or self.min_score.data < 0):
                self.min_score.errors.append("Minimum score required for score-based lottery")
                return False

        return True