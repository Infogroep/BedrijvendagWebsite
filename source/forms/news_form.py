from wtforms import Form, TextAreaField, StringField, validators


class news_form(Form):

	title = StringField('Title', validators=[validators.input_required(message='A title should be given')])
	news = TextAreaField('News', validators=[validators.input_required(message='Your news item needs a body')])