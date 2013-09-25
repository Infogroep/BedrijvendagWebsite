from database import *
from password import *
import bottle_session
import bottle
# Use Jinja2 as the template engine, allows for more extensive templates, like inheritance. http://jinja.pocoo.org/docs/
from bottle import jinja2_view as view, jinja2_template as template, static_file, request
from os.path import dirname, abspath

app = bottle.Bottle()
plugin = bottle_session.SessionPlugin(cookie_lifetime=300)
app.install(plugin)

ROOT = dirname(abspath(__file__)) + '/static'

#initialise()


@app.route('/')
def index():
    return template('static/templates/index_inherit.html', news_feed_query = get_news_feed())

@app.route('/pricelist')
def pricelist():
    return template('static/templates/pricelist_inherit.html')

@app.route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath,root= ROOT)

@app.route('/register')
def register_form():
    return template('static/templates/register_inherit.html')

@app.route('/company/<name>')
def company_page(name):
    #if (not session):
       # if(name == session.get('name')):
    company_ = company(name)
    return template('static/templates/company_page.html')
       # else:
    #        redirect('/401')
    #else:
    #    redirect('/401')

@app.route('/401')
def unauthorized():
    return template('static/templates/error_inherit.html', error = "You don't have the right permission")

@app.route('/register', method='post')
def register():
    name = request.forms.get('name')
    password = request.forms.get('password')
    hashed_password = encrypt(password)
    hashed_retype_password = encrypt(request.forms.get('password2'))
    print hashed_password, hashed_retype_password
    if hashed_password != hashed_retype_password:
        return template('static/templates/register_inherit.html', error = True, message = "Passwords did not match")
    company_ = company(name)
    if company_:
        add_login(name, hashed_password)
        return template('static/templates/login_inherit.html')
    else:
        return template('static/templates/register2_inherit.html', name = name, password = password)

@app.route('/register2', method='post')
def register2():
    return template('static/templates/index_inherit.html', news_feed_query = get_news_feed())

@app.route('/login')
def login_form():
    return template('static/templates/login_inherit.html')

@app.route('/login', method='post')
def login():
    #check it
    name = request.form.get('name')
    password = encrypt(request.form.get('password'))
    return_adress = 'static/templates/company/%s'
    return_adress = return_addres % name
    return template(return_adress)
