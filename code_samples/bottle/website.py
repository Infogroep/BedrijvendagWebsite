import bottle
# Use Jinja2 as the template engine, allows for more extensive templates, like inheritance. http://jinja.pocoo.org/docs/
from bottle import jinja2_view as view, jinja2_template as template


app = bottle.Bottle()

@app.route('/')
def index(name='main'):
    return template('<b>hello <name></b>')

@app.route('/hello/<name>')
def index(name='World'):
    return template('<b>Hello {{name}}</b>!', name=name)
