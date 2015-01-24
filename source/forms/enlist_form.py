import database
from wtforms import Form, BooleanField, SelectField, IntegerField, TextAreaField, validators


class enlist_update_form(Form):
	
	def get_formulas():
		formulas = database.get_formulas()

		res = []
		for fid, fname, fprice in formulas:
			res.append((fid, fname))

		return res

	formulas = get_formulas()
	formula = SelectField('Formula', choices=formulas)
	high_stand = BooleanField('High stand', description='Stands with a height larger then 2,1 meters are limited')
	tables = IntegerField('Number of tables', validators=[validators.input_required(message='Please give a requested number of tables')])
	promo = IntegerField('Number of promotion wands', validators=[validators.input_required(message='Please give a number of promotion wands')])
	remarks = TextAreaField('Remarks', validators=[validators.optional()])
