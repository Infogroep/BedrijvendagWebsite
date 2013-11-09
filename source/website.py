from database import *
from password import *
from bedrijvendagboek import *
import beaker.middleware
# Use Jinja2 as the template engine, allows for more extensive templates, like inheritance. http://jinja.pocoo.org/docs/
import datetime, resume
import bottle, logo, re, participant_converter
from config import *
from bottle import jinja2_view as view, jinja2_template as template, static_file, request, app
from bottle_flash import FlashPlugin
from bottle import Jinja2Template
from os.path import dirname, abspath

#app = bottle.Bottle()

STATIC = ROOT + '/static'

session_opts = {
    'session.type': 'file',
    'session.data_dir': './session/',
    'session.cookie_expires': 900,
    'session.auto': True,
}

app = beaker.middleware.SessionMiddleware(bottle.app(), session_opts)

message_flash = FlashPlugin(key='messages', secret=secret_key)
Jinja2Template.defaults["get_flashed_messages"] = message_flash.get_flashed_messages
Jinja2Template.settings["extensions"] =  ["jinja2.ext.with_"]
initialise.initialise()

@bottle.hook('before_request')
def setup_session():
    request.session = bottle.request.environ.get('beaker.session')

@bottle.route('/')
def index():
    '''returns static template index'''
    return template('static/templates/index_inherit.html', news_feed_query = get_news_feed(), edition = edition, name=request.session.get('logged_in'), admin=(True if request.session.get('logged_in') in admin_users.values() else False))

@bottle.route('/pricelist')
def pricelist():
    '''retuns static template pricelist'''
    return template('static/templates/pricelist_inherit.html', edition = edition, name=request.session.get('logged_in'), admin=(True if request.session.get('logged_in') in admin_users.values() else False))

@bottle.route('/static/<filepath:path>')
def server_static(filepath):
    '''routing to statci files: css, javascript'''
    return static_file(filepath,root= STATIC)

@bottle.route('/logos/<filepath:path>')
def server_log(filepath):
    '''routing to logos'''
    return static_file(filepath, root = STATIC)

@bottle.route('/register')
def register_form():
    '''returns the static register form'''
    return template('static/templates/register_inherit.html', edition = edition, name=request.session.get('logged_in'), admin=(True if request.session.get('logged_in') in admin_users.values() else False))

@bottle.route('/resume')
def resume_form():
    '''returns the static resume form'''
    return template('static/templates/resume_inherit.html', fields = fields_of_study, edition = edition, name=request.session.get('logged_in'), admin=(True if request.session.get('logged_in') in admin_users.values() else False)) 

@bottle.route('/resume', method="post")
def resume_upload():
    '''Uploading of the resume
    alle parameters are checked on server side
    resume gets stored in the directory of uploaders
    field of study
    '''

    resume_file = request.files.resume
    field = request.forms.get('studierichting')
    enrollment_number = request.forms.get('rolnummer')
    pattern = re.compile('[0-9]+')

    if enrollment_number == "":
        message_flash.flash("Please fill in your enrollment number", 'error')
        bottle.redirect('/resume')
    elif (not pattern.match(enrollment_number)):
        message_flash.flash("This field is numbers only", 'error')
        bottle.redirect('/resume')
    if resume_file:
        if (not resume_file.filename.endswith("pdf")):
            message_flash.flash("Your resume must be a pdf", 'error')
            bottle.redirect('/resume')
        else:
            resume.upload(field, enrollment_number, resume_file.file.read())
            message_flash.flash("Thank you for uploading your resume", 'success')
            bottle.redirect('/resume')
    else:
        message_flash.flash("You forgot to upload your resume", 'error')
        bottle.redirect('/resume')
 
@bottle.route('/company/<name>')
def company_page(name):
    '''routing to company's page where he can view it's information'''

    if (request.session.get('logged_in') == name):
        company_ = company(name)
        logo = get_logo(name)
        address = company_[2]
        postal = company_[3]
        place = company_[4]
        country = company_[5]
        tav = company_[6]
        email = company_[7]
        tel = company_[8]
        fax = company_[9]
        cell = company_[10]
        website = company_[11]
        
        if logo:
            logo = '''<img src="/%s">''' % logo
        else:
            logo = '''You have yet to upload your logo, go to the <a href="edit">edit page</a>'''
         
        if fax is None:
            fax = ""
        if tel is None:
            tel = ""
        if cell is None:
            cell = ""
        
        return template('static/templates/company_page_inherit.html', \
                        address = address, postal = postal, \
                        place = place, website = website, tav = tav, \
                        tel = tel, fax = fax, email = email, cell = cell, \
                        edition = edition, logo = logo, country = country, name=request.session.get('logged_in'), admin=(True if request.session.get('logged_in') in admin_users.values() else False))
    else:
        bottle.redirect('/unauthorized')

@bottle.route('/company/<name>/edit')
def company_page(name):
    '''routing to company's page where he can edit it's information'''

    if (request.session.get('logged_in') == name):
        company_ = company(name)
        logo = get_logo(name)
        address = company_[2]
        postal = company_[3]
        place = company_[4]
        country = company_[5]
        tav = company_[6]
        email = company_[7]
        tel = company_[8]
        fax = company_[9]
        cell = company_[10]
        website = company_[11]
        
        if logo:
            logo = '''<img src="/%s">''' % logo
        else:
            logo = '''You have yet to upload your logo'''
         
        if fax is None:
            fax = ""
        if tel is None:
            tel = ""
        if cell is None:
            cell = ""
        
        return template('static/templates/company_page_edit_inherit.html', \
                        address = address, postal = postal, \
                        place = place, website = website, tav = tav, \
                        tel = tel, fax = fax, email = email, cell = cell, \
                        edition = edition, logo = logo, country = country, name=request.session.get('logged_in'), admin=(True if request.session.get('logged_in') in admin_users.values() else False))
    else:
        bottle.redirect('/unauthorized')

@bottle.route('/company/<name>/logout')
def logout(name):
    '''ends the company's session'''
    
    try:
        request.session.delete()
        bottle.redirect('/login')
    except KeyError:
        bottle.redirect('/unauthorized')

@bottle.route('/company/<name>/companiesbook')
def companiesbook(name):
    '''returns the companies book form'''
    
    if(request.session.get('logged_in') == name):
        return template('static/templates/companiesbook_inherit.html', edition = edition, name=request.session.get('logged_in'), admin=(True if request.session.get('logged_in') in admin_users.values() else False))
    else:
        bottle.redirect('/unauthorized')

@bottle.route('/company/<name>/companiesbook', method='post')
def static_company_page(name):
    '''Fetches the data from the form
    uses this to create his page'''

    if(request.session.get('logged_in') == name):
        location = request.forms.get('location')
        slogan = request.forms.get('slogan')
        why = request.forms.get('why')
        field = request.forms.get('schooling')
        develop = request.forms.get('develop')
        NL = bool(request.forms.get('NL'))
        FR = bool(request.forms.get('FR'))
        DE = bool(request.forms.get('DE'))
        ENG = bool(request.forms.get('ENG'))
        JOBS = bool(request.forms.get('JOBS'))
        SJOBS = bool(request.forms.get('SJOBS'))
        STAGE = bool(request.forms.get('STAGE'))
        FY = bool(request.forms.get('FY'))
        CH = bool(request.forms.get('CH'))
        WI = bool(request.forms.get('WI'))
        BIO = bool(request.forms.get('BIO'))
        CW = bool(request.forms.get('CW'))
        BIN = bool(request.forms.get('BIN'))
        GEO = bool(request.forms.get('GEO'))


        create_tex_file(name, location, slogan, why, NL, ENG, FR, DE, JOBS, STAGE, SJOBS, field, develop, FY, CH, WI, BIO, CW, BIN, GEO)
        return template('static/templates/companiesbook_inherit.html', edition = edition, name=request.session.get('logged_in'), admin=(True if request.session.get('logged_in') in admin_users.values() else False))
    else:
        bottle.redirect('/unauthorized')

    
    bottle.redirect('''/company/%s/companiesbook''' % name)

@bottle.route('/company/<name>/logo', method='post')
def upload(name):
    '''Fetches the logo send by the company
    and stores it resizes it and saves both
    resized and original folder'''


    if(request.session.get('logged_in') == name):
        img = request.files.logo

        if img:
            raw = img.file.read()
            img_file = open(logo.original_logo(img.filename), 'w')
            img_file.write(raw)
            img_file.close()
            logo.resize_logo(img.filename)
            set_logo(name, logo.resized_logo(img.filename))
        bottle.redirect('/company/%s/edit' % name)
    else:
        bottle.redirect('/unauthorized')

@bottle.route('/company/<name>/update/<column>', method='post')
def update_(name, column):
    '''update given column of given company'''

    if(request.session.get('logged_in') == name):
        value = request.forms.get('value')
        update(name, value, column)
        bottle.redirect('/company/%s' % name)
    else:
        bottle.redirect('/unauthorized')

@bottle.route('/company/<name>/enlist')
def enlist_form(name):
    '''returns the enlist form'''


    if(request.session.get('logged_in') == name):
        participating = is_participant(name, edition)
        state = None
        stateID = None
        formulaID = None
        formula = None
        tables = None
        promo = None
        remarks = None
        high = None
        
        if participating:
            state = get_status(name, edition)
            formulaID = get_formula(name, edition)
            formula = get_formula_by_id(formulaID)
            stateID = participant_converter.state_to_id(state)

            ID = get_companyID(name)
            participant = get_participant(ID, edition)

            # This is ugly and wrong and I am ashamed but fuck it
            # Deadline is long due

            tables = participant[4]
            promo = participant[5]
            remarks = participant[6]
            high = participant[7]


        return template('static/templates/enlist_inherit.html', options = get_formulas(), \
                                                                participant = participating, \
                                                                state = state, \
                                                                stateID = stateID, \
                                                                formula = formula, \
                                                                formulaID = formulaID, \
                                                                confirmed = requested_contract(name), \
                                                                tables = tables, \
                                                                promo = promo, \
                                                                remarks = remarks, \
                                                                high = high, \
                                                                edition = edition, name=request.session.get('logged_in'), admin=(True if request.session.get('logged_in') in admin_users.values() else False))
    else:
        bottle.redirect('/unauthorized')

@bottle.route('/company/<name>/enlist', method='post')
def enlist(name):
    '''uses the posted information to make the
    company a participant or to change
    it's settings'''

    
    if(request.session.get('logged_in') == name):
        formula = request.forms.get('formula')
        high = request.forms.get('high')
        print "enlist", formula, high
        if (not high == "1"):
            high = 0

        if is_participant(name, edition):
            tables = request.forms.get('table')
            promo_wands = request.forms.get('promo_wand')
            remarks = request.forms.get('remarks')
            edit_participant(name, edition, formula, high, tables, promo_wands, remarks)
        else: 
            add_participant(name, edition, formula, high)
        bottle.redirect('/company/%s/enlist' % (name,))
    else:
        bottle.redirect('/unauthorized')

@bottle.route('/company/<name>/confirm')
def confirm(name):
    '''Confirm the participant settings, request contract'''

    if(request.session.get('logged_in') == name):

        state = participant_converter.state_to_id(get_status(name, edition))

        # if subscription confirmed
        if state == 2:
            change_participant_status(name, edition, participant_converter.id_to_state(3))
        else:
            return template('static/templates/error_inherit.html', error = "You can't request your contract in your current state" , edition = edition, name=request.session.get('logged_in'), admin=(True if request.session.get('logged_in') in admin_users.values() else False))
        
        bottle.redirect('''/company/%s/enlist''' % (name,))

    else:
        bottle.redirect('/unauthorized')

@bottle.route('/unauthorized')
def unauthorized():
    '''retuns the page showing the unauthorized message'''
    return template('static/templates/error_inherit.html', error = "You don't have the right permission", edition = edition, name=request.session.get('logged_in'), admin=(True if request.session.get('logged_in') in admin_users.values() else False))

@bottle.route('/register', method='post')
def register():
    '''uses the posted information to create a new company'''

    name = request.forms.get('name')
    password = request.forms.get('password')
    hashed_password = encrypt(password)
    retype_password = request.forms.get('retype_password')
    
    if (not is_equal(hashed_password, retype_password)):
        return template('static/templates/register_inherit.html', error = True, message = "Passwords did not match", edition = edition, name=request.session.get('logged_in'), admin=(True if request.session.get('logged_in') in admin_users.values() else False))
    company_ = company(name)
    if company_:
        return template('static/templates/register_inherit.html', error = True, message = "An account with this company already exists", edition = edition, name=request.session.get('logged_in'), admin=(True if request.session.get('logged_in') in admin_users.values() else False))
    else:
        
        address = request.forms.get('address')
        zipcode = request.forms.get('zipcode')
        city = request.forms.get('city')
        country = request.forms.get('country')
        tav = request.forms.get('tav')
        email = request.forms.get('email')
        tel = request.forms.get('tel')
        fax = request.forms.get('fax')
        cell = request.forms.get('cell')
        website = request.forms.get('website')

        error = ""

        tel_pattern = re.compile('^[0-9]{2}/?[0-9]{3}.?[0-9]{2,3}.?[0-9]{2,3}$')

        
        if name == "":
           error += "The name field may not be empty <br>"
           #return template('static/templates/register_inherit.html', error = True, message = "The name field may not be empty", name=request.session.get('logged_in'), admin=(True if request.session.get('logged_in') in admin_users.values() else False))
        if (password == ""):
           error += "The password field may not be empty <br>"
        if address == "":
           error += "The address field may not be empty <br>"
           #return template('static/templates/register_inherit.html', error = True, message = "The address field may not be empty", name=request.session.get('logged_in'), admin=(True if request.session.get('logged_in') in admin_users.values() else False))
        if zipcode == "":
           error += "The postal code field may not be empty <br>"
           #return template('static/templates/register_inherit.html', error = True, message = "The postal code field may not be empty", name=request.session.get('logged_in'), admin=(True if request.session.get('logged_in') in admin_users.values() else False))
        if city == "":
           error += "The city field may not be empty <br>"
           #return template('static/templates/register_inherit.html', error = True, message = "The city field may not be empty", name=request.session.get('logged_in'), admin=(True if request.session.get('logged_in') in admin_users.values() else False))
        if country == "":
           error += "The country field may not be empty <br>"
           #return template('static/templates/register_inherit.html', error = True, message = "The country field may not be empty", name=request.session.get('logged_in'), admin=(True if request.session.get('logged_in') in admin_users.values() else False))
        if tav == "":
           error += "The contact person field may not be empty <br>"
           #return template('static/templates/register_inherit.html', error = True, message = "The contact person field may not be empty", name=request.session.get('logged_in'), admin=(True if request.session.get('logged_in') in admin_users.values() else False))
        if email == "":
           error += "The email field may not be empty <br>"
           #return template('static/templates/register_inherit.html', error = True, message = "The email field may not be empty", name=request.session.get('logged_in'), admin=(True if request.session.get('logged_in') in admin_users.values() else False))
        if website == "":
           error += "The website field may not be empty <br>"
           #return template('static/templates/register_inherit.html', error = True, message = "The website field may not be empty", name=request.session.get('logged_in'), admin=(True if request.session.get('logged_in') in admin_users.values() else False))
        if tel != "":
            tel = re.sub('\s*', '', tel)
            if not (tel_pattern.match(tel)):
                error += "Given telephone number appeared to be incorrect </br>"
        if fax != "":
            fax = re.sub('\s*', '', fax)
            if not (tel_pattern.match(fax)):
                error += "Given fax number appeared to be incorrect </br>"
        if cell != "":
            cell = re.sub('\s*', '', cell)
            if not (tel_pattern.match(cell)):
                error += "Given cellphone number appeared to be incorrect </br>"

        if error == "":
            try:
                if int(zipcode) > 0:
                    add_company(name, address, zipcode, city, country, tav, email, tel, fax, cell, website)
                    add_login(name, hashed_password)
                    bottle.redirect('/login')
                else:
                    return template('static/templates/register_inherit.html', error = True, message = "The postal code may not be a negative number", name=request.session.get('logged_in'), admin=(True if request.session.get('logged_in') in admin_users.values() else False))
            except:
                return template('static/templates/register_inherit.html', error = True, message = "The postal code field must be a number", name=request.session.get('logged_in'), admin=(True if request.session.get('logged_in') in admin_users.values() else False))
        else:
            return template('static/templates/register_inherit.html', error = True, message = error, name=request.session.get('logged_in'), admin=(True if request.session.get('logged_in') in admin_users.values() else False))


@bottle.route('/login')
def login_form():
    '''shows the login form'''

    return template('static/templates/login_inherit.html', edition = edition, name=request.session.get('logged_in'), admin=(True if request.session.get('logged_in') in admin_users.values() else False))

@bottle.route('/login', method='post')
def login_():
    '''Start a new session'''
    
    name = request.forms.get('name')
    password = request.forms.get('password')
    
    route_address = '/company/%s'
    route_address = route_address % name
    
    if name in admin_users:
        route_address = '/' + admin_users[name]
        name = admin_users[name]
    
    if(login(name, password)):
        
        request.session["logged_in"] = name
        bottle.redirect(route_address)
    else:
        message_flash.flash('The company/password combination is incorrect', 'alert')
        bottle.redirect('/login')

@bottle.route('/<name>')
def admin_page(name):
    '''returns the admin page'''

    if(name in admin_users.values() and request.session.get('logged_in') == name):
        return template('static/templates/infogroep_inherit.html', edition = edition, news_feed_query = get_news_feed(), name=request.session.get('logged_in'), admin=(True if request.session.get('logged_in') in admin_users.values() else False))
    else:
        bottle.redirect('/unauthorized')

    
@bottle.route('/add news', method='post')
def addnews():
    '''Add a new news item'''

    short = request.forms.get('short')
    news = request.forms.get('news')
    
    add_news_item(short, news)
    
    bottle.redirect('/infogroep')

@bottle.route('/<name>/participants')
def admin_participants(name):
    '''Show and edit participant information'''

    if(name in admin_users.values() and request.session.get('logged_in') == name):
        return template('static/templates/admin_participants.html', edition = edition, participants = get_participants(edition), name=request.session.get('logged_in'), admin=(True if request.session.get('logged_in') in admin_users.values() else False))
    else:
        bottle.redirect('/unauthorized')
    
@bottle.route('/<name>/participants/setstate/<company>/<state>')
def set_state(name, company, state):
    '''change the state of the company'''

    if(name in admin_users.values() and request.session.get('logged_in') == name):
        state = participant_converter.id_to_state(state)
        
        change_participant_status(company, edition, state)
        bottle.redirect('/%s/participants' % (name))
    else:
        bottle.redirect('/unauthorized')


@bottle.route('/infogroep/delete_news/<id>')
def remove_news_item_site(id):

    
    if(request.session.get('logged_in') == "infogroep"):
        remove_news_item(id)
        bottle.redirect('/infogroep')
    else:
        bottle.redirect('/unauthorized')

#bottle.run(app)
