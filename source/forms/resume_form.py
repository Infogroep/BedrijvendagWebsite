import config, re
from wtforms import Form, FileField, StringField, SelectField, IntegerField, validators, ValidationError

class resume_form(Form):


	def validate_resume(form, field):
		if not(field.data.filename.endswith('.pdf')):
			raise ValidationError('File must be a pdf')

	enrollment_number = StringField('Enrollment number', validators=[validators.input_required(message='Your enrollment number is required'),\
																	 validators.regexp('^[0-9]{5,6}$', message='Your enrollment number is a number of 5 to 6 digits')])
	field_of_study = SelectField('Field of study', choices=config.fields_of_study)
	resume = FileField('Upload resume', validators=[validators.input_required(message='You need a resume to upload')])

