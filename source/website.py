from database import *
import bottle_session
import bottle
# Use Jinja2 as the template engine, allows for more extensive templates, like inheritance. http://jinja.pocoo.org/docs/
from bottle import jinja2_view as view, jinja2_template as template, static_file, request
from os.path import dirname, abspath

app = bottle.Bottle()

ROOT = dirname(abspath(__file__)) + '/static'

#initialise()

print ROOT

@app.route('/')
def index():
    return template('static/templates/index_inherit.html', news_feed_query = get_news_feed())

@app.route('/pricelist')
def pricelist():
    return template('static/templates/pricelist_inherit.html')

@app.route('/static/<filepath:path>')
def server_static(filepath):
    print filepath
    return static_file(filepath,root= ROOT)

@app.route('/register')
def register_form():
    return template('static/templates/register_inherit.html')

@app.route('/register', method='post')
def register():
    print request.forms.get('name')
    return template('static/templates/register_inherit.html')
