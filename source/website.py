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
import forms.registration_form as registration_form, forms.resume_form as resume_form
import forms.login_form as login_form

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

@bottle.route('/about')
def about():
    '''Returns the about page'''
    return template('static/templates/about_inherit.html', edition = edition, name = request.session.get('logged_in'), admin=(True if request.session.get('logged_in') in admin_users.values() else False))

@bottle.route('/when_and_where')
def when_and_where():
    '''Returns the when and where page'''
    return template('static/templates/when_where_inherit.html', edition = edition, name = request.session.get('logged_in'), admin=(True if request.session.get('logged_in') in admin_users.values() else False))

@bottle.route('/tombola')
def when_and_where():
    '''Returns the when and where page'''
    return template('static/templates/tombola_inherit.html', edition = edition, name = request.session.get('logged_in'), admin=(True if request.session.get('logged_in') in admin_users.values() else False))

@bottle.route('/participants')
def participants():
    '''retuns all the participating companies (after signed contract has been received)'''
    return template('static/templates/participants_inherit.html', edition = edition, name = request.session.get('logged_in'), admin=(True if request.session.get('logged_in') in admin_users.values() else False))


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

    form = registration_form.RegistrationForm()
    #form.content('class="form-control"')

    return template('static/templates/register_inherit.html', edition = edition, form = form, name=request.session.get('logged_in'), admin=(True if request.session.get('logged_in') in admin_users.values() else False))

@bottle.route('/resume')
def resume_form_route():
    '''returns the static resume form'''

    form = resume_form.resume_form()
    return template('static/templates/resume_inherit.html', form=form, edition = edition, name=request.session.get('logged_in'), admin=(True if request.session.get('logged_in') in admin_users.values() else False)) 

@bottle.route('/resume', method="post")
def resume_upload():
    '''Uploading of the resume
    alle parameters are checked on server side
    resume gets stored in the directory of uploaders
    field of study
    '''

    form=resume_form.resume_form(request.POST)

    if form.validate():
        resume.upload(form.field_of_study.data, form.enrollment_number.data, form.resume.data.file.read())
        message_flash.flash('Thank you for uploading your resume', 'success')
        bottle.redirect('/resume')
    else:
        for field_name in form.errors:
            for error in form.errors[field_name]:
                message_flash.flash(error, 'danger')
        return template('static/templates/resume_inherit.html', form=form, edition = edition, name=request.session.get('logged_in'), admin=(True if request.session.get('logged_in') in admin_users.values() else False))

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
            logo = '''You have yet to upload your logo, go to the <a href="/company/%s/edit">edit page</a>''' % name
         
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

    form = registration_form.RegistrationForm(request.POST)

    if form.validate():

        add_company(form.company_name.data, form.address.data, form.postal.data, form.city.data, form.country.data,\
                    form.contact.data, form.email.data, form.tel.data, form.fax.data, form.cel.data, form.website.data, encrypt(form.password.data))
        message_flash.flash('Your account has been created.', 'succes')
        bottle.redirect('/login')
    else:
        message = ''
        for field_name in form.errors:
            for error in form.errors[field_name]:
                message += '%s </br>' % error
        message_flash.flash(message, 'danger')
        return template('static/templates/register_inherit.html', edition = edition, form = form, name=request.session.get('logged_in'), admin=(True if request.session.get('logged_in') in admin_users.values() else False))


@bottle.route('/login')
def login_form_route():
    '''shows the login form'''
    form = login_form.login_form()

    return template('static/templates/login_inherit.html', form=form, edition = edition, name=request.session.get('logged_in'), admin=(True if request.session.get('logged_in') in admin_users.values() else False))

@bottle.route('/login', method='post')
def login_():
    '''Start a new session'''

    form = login_form.login_form(request.POST)
    
    if form.validate():
        name = form.company_name.data
        password = form.password.data
        
        route_address = '/company/%s'
        route_address = route_address % name
        
        if name in admin_users:
            route_address = '/' + admin_users[name]
        
        if(login(name, password)):
            
            request.session["logged_in"] = (name if name not in admin_users else admin_users[name])
            bottle.redirect(route_address)
        else:
            message_flash.flash('The company/password combination is incorrect', 'danger')
            return template('static/templates/login_inherit.html', form=form, edition = edition, name=request.session.get('logged_in'), admin=(True if request.session.get('logged_in') in admin_users.values() else False))

    else:
        message=""
        for field_name in form.errors:
            for error in form.errors[field_name]:
                message += error
                message += '</br>'
        message_flash.flash(message, 'danger')
        bottle.redirect('/login')


@bottle.route('/recover/<hash>')
def recover_password(hash):
    company_ = find_password_hash(hash)

    if company:
        return template('static/templates/password_recovery_inherit.html', edition = edition, name=request.session.get('logged_in'), admin=(True if request.session.get('logged_in') in admin_users.values() else False), hash=hash)
    else:
        bottle.redirect('/unauthorized')

@bottle.route('/recover/<hash>', method='post')
def change_password_url(hash):
    company_ = find_password_hash(hash)

    password = request.forms.get('password')
    hashed_password = encrypt(password)
    retype_password = request.forms.get('password_confirm')
    if (not is_equal(hashed_password, retype_password)):
        message_flash.flash("Passwords did not match", 'danger')
        bottle.redirect('/recover/%s' % hash)
    elif company_:
        change_password(company_, hashed_password)
        delete_password_hash(hash)
        message_flash.flash("Password changed successfully", 'success')
        bottle.redirect('/login')
    else:
        bottle.redirect('/unauthorized')

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
