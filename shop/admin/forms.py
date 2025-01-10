from wtforms import BooleanField, StringField, PasswordField, validators , ValidationError
from flask_wtf import FlaskForm, Form
from .models import User


class RegistrationForm(FlaskForm):
    name = StringField('Name', [validators.Length(min=4, max=25)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')


class LoginForm(FlaskForm):
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [validators.DataRequired()])