import re, database, password
from wtforms import Form, BooleanField, StringField, PasswordField, IntegerField, validators, ValidationError

class RegistrationForm(Form):

	def validate_address(form, field):
		address_pattern = re.compile('^[a-z]*, [0-9]*[a-z]{0,2}$')
		if address_pattern.match(field.data) is None:
			raise ValidationError("Your address seems to be incorrect. Streetname, housenumber")

	def validate_company_name(form, field):
		company = database.company(field.data)

		if company:
			raise ValidationError("An account for this company already exists")


	company_name = StringField('Company name', validators=[validators.input_required(message="company name is required")])
	password = PasswordField('Password', validators=[validators.input_required(message="Password is required")])
	retype_password = PasswordField('Retype password', validators=[validators.input_required(message="Retype password is required"), validators.EqualTo("password", message="Passwords do not match")])
	address = StringField('Address', validators=[validators.input_required(message="Address is required")])
	postal = IntegerField('Postal', validators=[validators.input_required(message="Zipcode is required. It may only consist of number")])
	city = StringField('City', validators=[validators.input_required(message="City is required")])
	country = StringField('Country', validators=[validators.input_required(message="Country is required")])
	contact = StringField('Contact person', validators=[validators.input_required(message="Contact is required")])
	email = StringField('Email address', validators=[validators.input_required(message="Email is required"), validators.Email(message="Invalid email address")])
	website = StringField('Website', validators=[validators.input_required(message="Website is required"), validators.URL(message="Invalid website")])
	tel = StringField('Telephone number', validators=[validators.required(message="Telephone number is required, numbers only"), validators.Length(min=9, max=12, message="Length doesn't match telephone number length")])
	fax = StringField('Fax number', validators=[validators.optional(), validators.Length(min=9, max=12, message="Length doesn't match fax number length")])
	cel = StringField('Cellphone number', validators=[validators.optional(), validators.Length(min=9, max=12, message="Length doesn't match cellphone number length")])



