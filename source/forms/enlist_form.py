from wtforms import Form, BooleanField, StringField, PasswordField, IntegerField, validators, ValidationError

class enlist_form(Form):
	
	tables = IntField('Number of tables', message="Number of tables must be an integer",\
					   validators=[validators.validators]
					  )