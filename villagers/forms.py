from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class UserSignupForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    first_name = StringField('First Name', validators = [DataRequired()])
    last_name = StringField('Last Name', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit_button = SubmitField('SIGN UP')

class UserSigninForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit_button = SubmitField('SIGN IN')

class VillagerForm(FlaskForm):
    name = StringField('Name', validators = [DataRequired()])
    species = StringField('Species', validators = [DataRequired()])
    submit_button = SubmitField('ADD')

class SearchForm(FlaskForm):
    search = StringField('Species', validators= [DataRequired()])
    submit_button = SubmitField('SEARCH')  