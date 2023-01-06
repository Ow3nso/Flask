import email
from tokenize import String
from flask_wtf import FlaskForm
from jsonschema import ValidationError
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from market import User

class RegistrationForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email address already exists')

    username = StringField('Username', 
                            validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', 
                                validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                                    validators=[DataRequired(), EqualTo('password')])
    email_address = StringField('Email', 
                                validators=[Email(), DataRequired()])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
   
    password = PasswordField('Password', 
                            validators=[DataRequired(), ])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')