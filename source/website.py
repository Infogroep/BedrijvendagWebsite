from database import *
from password import *
from bedrijvendagboek import *
import beaker.middleware
# Use Jinja2 as the template engine, allows for more extensive templates, like inheritance. http://jinja.pocoo.org/docs/
import datetime, resume
import bottle, logo, re, participant_converter
from config import *
from bottle import jinja2_view as view, jinja2_template as template, static_file, request, app
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

initialise.initialise()

@bottle.route('/')
def index():
    '''returns static template index'''
    return template('static/templates/index_inherit.html', news_feed_query = get_news_feed(), edition = edition)

@bottle.route('/pricelist')
def pricelist():
    '''retuns static template pricelist'''
    return template('static/templates/pricelist_inherit.html', edition = edition)

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
    return template('static/templates/register_inherit.html', edition = edition)

@bottle.route('/resume')
def resume_form():
    '''returns the static resume form'''
    return template('static/templates/resume_inherit.html', fields = fields_of_study, edition = edition) 

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
        return template('static/templates/resume_inherit.html', edition = edition, fields = fields_of_study, error = True, message = "Please fill in your enrollment number")
    elif (not pattern.match(enrollment_number)):
        return template('static/templates/resume_inherit.html', edition = edition, fields = fields_of_study, error = True, message = "Enrollment number are numbers only")
    
    if resume_file:
        if (not resume_file.filename.endswith("pdf")):
            return template('static/templates/resume_inherit.html', edition = edition, fields = fields_of_study, error = True, message = "Your resume must be a pdf file")
        else:
            resume.upload(field, enrollment_number, resume_file.file.read())
            return template('static/templates/resume_inherit.html', edition = edition, fields = fields_of_study, succes = True, message = "We are most gratefull for your precious resume")
    else:
        return template('static/templates/resume_inherit.html', edition = edition, fields = fields_of_study, error = True, message = "Your resume, ... you forgot to select it")

 



@bottle.route('/company/<name>')
def company_page(name):
    '''routing to company's page where he can view it's information'''

    session = bottle.request.environ.get('beaker.session')
    try:
        if (session[name] == True):
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
            
            return template('static/templates/company_page_inherit.html', \
                            name = name, address = address, postal = postal, \
                            place = place, website = website, tav = tav, \
                            tel = tel, fax = fax, email = email, cell = cell, \
                            edition = edition, logo = logo, country = country)
        else:
            bottle.redirect('/unauthorized')
    except KeyError:
        bottle.redirect('/unauthorized')

@bottle.route('/company/<name>/edit')
def company_page(name):
    '''routing to company's page where he can edit it's information'''

    session = bottle.request.environ.get('beaker.session')
    try:
        if (session[name] == True):
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
                            name = name, address = address, postal = postal, \
                            place = place, website = website, tav = tav, \
                            tel = tel, fax = fax, email = email, cell = cell, \
                            edition = edition, logo = logo, country = country)
        else:
            bottle.redirect('/unauthorized')
    except KeyError:
        bottle.redirect('/unauthorized')


@bottle.route('/company/<name>/logout')
def logout(name):
    '''ends the company's session'''
    session = bottle.request.environ.get('beaker.session')
    try:
        session[name] = False
        bottle.redirect('/login')
    except KeyError:
        bottle.redirect('/unauthorized')

@bottle.route('/company/<name>/companiesbook')
def companiesbook(name):
    '''returns the companies book form'''
    session = bottle.request.environ.get('beaker.session')
    try:
        if(session[name] == True):
            return template('static/templates/companiesbook_inherit.html', name = name, edition = edition)
        else:
            bottle.redirect('/unauthorized')
    except KeyError:
        bottle.redirect('/unauthorized')

@bottle.route('/company/<name>/companiesbook', method='post')
def static_company_page(name):
    session = bottle.request.environ.get('beaker.session')
    try:
        if(session[name] == True):
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
            return template('static/templates/companiesbook_inherit.html', name = name, edition = edition)
        else:
            bottle.redirect('/unauthorized')
    except KeyError:
        bottle.redirect('/unauthorized')
    
    bottle.redirect('''/company/%s/companiesbook''' % name)

@bottle.route('/company/<name>/logo', method='post')
def upload(name):
    session = bottle.request.environ.get('beaker.session')
    try:
        if(session[name] == True):
            img = request.files.logo

            if img:
                raw = img.file.read()
                img_file = open(logo.original_logo(img.filename), 'w')
                img_file.write(raw)
                img_file.close()
                logo.resize_logo(img.filename)
                set_logo(name, logo.resized_logo(img.filename))
            bottle.redirect('/company/edit%s' % name)
        else:
            bottle.redirect('/unauthorized')
    except KeyError:
        bottle.redirect('/unauthorized')

@bottle.route('/company/<name>/update/<column>', method='post')
def update_(name, column):
    session = bottle.request.environ.get('beaker.session')
    try:
        if(session[name] == True):
            value = request.forms.get('value')
            update(name, value, column)
            bottle.redirect('/company/%s' % name)
        else:
            bottle.redirect('/unauthorized')
    except KeyError:
        bottle.redirect('/unauthorized')

@bottle.route('/company/<name>/enlist')
def enlist_form(name):
    session = bottle.request.environ.get('beaker.session')
    try:
        if(session[name] == True):
            participating = is_participant(name, edition)
            state = None
            stateID = None
            formulaID = None
            formula = None
            
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


            return template('static/templates/enlist_inherit.html', options = get_formulas(), name = name, \
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
                                                                    edition = edition)
        else:
            bottle.redirect('/unauthorized')
    except KeyError:
        bottle.redirect('/unauthorized')

@bottle.route('/company/<name>/enlist', method='post')
def enlist(name):
    session = bottle.request.environ.get('beaker.session')
    try:
        if(session[name] == True):
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
    except KeyError:
        bottle.redirect('/unauthorized')


@bottle.route('/company/<name>/confirm')
def confirm(name):
    session = bottle.request.environ.get('beaker.session')
    try:
        if(session[name] == True):

            state = participant_converter.state_to_id(get_status(name, edition))

            # if subscription confirmed
            if state == 2:
                change_participant_status(name, edition, participant_converter.id_to_state(3))
            else:
                return template('static/templates/error_inherit.html', error = "You can't request your contract in your current state" , edition = edition)
            
            bottle.redirect('''/company/%s/enlist''' % (name,))

        else:
            bottle.redirect('/unauthorized')
    except KeyError:
        bottle.redirect('/unauthorized')


@bottle.route('/unauthorized')
def unauthorized():
    return template('static/templates/error_inherit.html', error = "You don't have the right permission", edition = edition)

@bottle.route('/register', method='post')
def register():
    name = request.forms.get('name')
    password = request.forms.get('password')
    hashed_password = encrypt(password)
    retype_password = request.forms.get('retype_password')
    
    if (not is_equal(hashed_password, retype_password)):
        return template('static/templates/register_inherit.html', error = True, message = "Passwords did not match", edition = edition)
    company_ = company(name)
    if company_:
        return template('static/templates/register_inherit.html', error = True, message = "An account with this company already exists", edition = edition)
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
        
        if name == "":
           return template('static/templates/register_inherit.html', error = True, message = "The name field may not be empty")
        elif address == "":
           return template('static/templates/register_inherit.html', error = True, message = "The address field may not be empty")
        elif zipcode == "":
           return template('static/templates/register_inherit.html', error = True, message = "The postal code field may not be empty")
        elif city == "":
           return template('static/templates/register_inherit.html', error = True, message = "The city field may not be empty")
        elif country == "":
           return template('static/templates/register_inherit.html', error = True, message = "The country field may not be empty")
        elif tav == "":
           return template('static/templates/register_inherit.html', error = True, message = "The contact person field may not be empty")
        elif email == "":
           return template('static/templates/register_inherit.html', error = True, message = "The email field may not be empty")
        elif website == "":
           return template('static/templates/register_inherit.html', error = True, message = "The website field may not be empty")
        else:
            add_company(name, address, zipcode, city, country, tav, email, tel, fax, cell, website)
            add_login(name, hashed_password)
            bottle.redirect('/login')

@bottle.route('/login')
def login_form():
    return template('static/templates/login_inherit.html', edition = edition)

@bottle.route('/login', method='post')
def login_():
    
    name = request.forms.get('name')
    password = request.forms.get('password')
    
    route_address = '/company/%s'
    route_address = route_address % name
    
    if (name == 'ig'):
        name = 'infogroep'
        route_address = '/' + name
    if (name == 'wk'):
        name = 'wetenschappelijke kring'
        route_address = '/' + name
    
    if(login(name, password)):
        session = bottle.request.environ.get('beaker.session')
        session[name] = True
        bottle.redirect(route_address)
    else:
        return template('static/templates/login_inherit', error=True, msg = "The given combination was incorrect")

@bottle.route('/<name>')
def admin_page(name):
    session = bottle.request.environ.get('beaker.session')
    try:
        if(session[name] == True):
            return template('static/templates/infogroep_inherit.html', name = "infogroep", edition = edition)
        else:
            bottle.redirect('/unauthorized')
    except KeyError:
        bottle.redirect('/unauthorized')
    
@bottle.route('/add news', method='post')
def addnews():
    short = request.forms.get('short')
    news = request.forms.get('news')
    
    add_news_item(short, news)
    
    bottle.redirect('/infogroep')

@bottle.route('/<name>/participants')
def admin_participants(name):
    session = bottle.request.environ.get('beaker.session')
    try:
        if(session[name] == True):
            return template('static/templates/admin_participants.html', name = name, edition = edition, participants = get_participants(edition))
        else:
            bottle.redirect('/unauthorized')
    except KeyError:
        bottle.redirect('/unauthorized')
    
@bottle.route('/<name>/participants/setstate/<company>/<state>')
def set_state(name, company, state):
    session = bottle.request.environ.get('beaker.session')
    try:
        if(session[name] == True):
            state = participant_converter.id_to_state(state)
            
            change_participant_status(company, edition, state)
            bottle.redirect('/%s/participants' % (name))
        else:
            bottle.redirect('/unauthorized')
    except KeyError:
        bottle.redirect('/unauthorized')