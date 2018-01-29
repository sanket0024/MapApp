from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators

class SignupForm(FlaskForm):
	first_name = StringField('First name', [validators.DataRequired()])
	last_name = StringField('Lats name', [validators.DataRequired()])
	email = StringField('Email', [validators.DataRequired(), validators.Email()])
	password = PasswordField('Password', [validators.Length(min=8, max=16)])
	submit = SubmitField('Sign up')