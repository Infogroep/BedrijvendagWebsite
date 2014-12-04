import database
from wtforms import Form, FileField, StringField, PasswordField, IntegerField, validators, ValidationError

class login_form(Form):

	company_name = StringField('Email address', validators=[validators.input_required('An email address is required to log in')])
	password = PasswordField('Password', validators=[validators.input_required('Password field is required')])
