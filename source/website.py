from database import *
from password import *
import beaker.middleware
# Use Jinja2 as the template engine, allows for more extensive templates, like inheritance. http://jinja.pocoo.org/docs/
import bottle
from bottle import jinja2_view as view, jinja2_template as template, static_file, request, app
from os.path import dirname, abspath

#app = bottle.Bottle()

ROOT = dirname(abspath(__file__)) + '/static'

session_opts = {
    'session.type': 'file',
    'session.data_dir': './session/',
    'session.auto': True,
}

app = beaker.middleware.SessionMiddleware(bottle.app(), session_opts)

#initialise()


@bottle.route('/')
def index():
    return template('static/templates/index_inherit.html', news_feed_query = get_news_feed())

@bottle.route('/pricelist')
def pricelist():
    return template('static/templates/pricelist_inherit.html')

@bottle.route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath,root= ROOT)

@bottle.route('/register')
def register_form():
    return template('static/templates/register_inherit.html')

@bottle.route('/company/<name>')
def company_page(name):
    #if (not session):
       # if(name == session.get('name')):
    company_ = company(name)
    return template('static/templates/company_page.html', name = name)
       # else:
    #        redirect('/401')
    #else:
    #    redirect('/401')

@bottle.route('/401')
def unauthorized():
    return template('static/templates/error_inherit.html', error = "You don't have the right permission")

@bottle.route('/register', method='post')
def register():
    name = request.forms.get('name')
    password = request.forms.get('password')
    hashed_password = encrypt(password)
    hashed_retype_password = encrypt(request.forms.get('password2'))
    
    if hashed_password != hashed_retype_password:
        return template('static/templates/register_inherit.html', error = True, message = "Passwords did not match")
    company_ = company(name)
    if company_:
        add_login(name, hashed_password)
        return template('static/templates/login_inherit.html')
    else:
        return template('static/templates/register2_inherit.html', name = name, password = password)

@bottle.route('/register2', method='post')
def register2():
    return template('static/templates/index_inherit.html', news_feed_query = get_news_feed())

@bottle.route('/login')
def login_form():
    return template('static/templates/login_inherit.html')

@bottle.route('/login', method='post')
def login():
    #check it
    name = request.form.get('name')
    password = encrypt(request.form.get('password'))
    return_adress = 'static/templates/company/%s'
    return_adress = return_addres % name
    return template(return_adress)
