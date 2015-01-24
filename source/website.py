#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bedrijvendagboek import *
import beaker.middleware
# Use Jinja2 as the template engine, allows for more extensive templates, like inheritance. http://jinja.pocoo.org/docs/
import resume
import bottle, logo, participant_converter
from config import *
from bottle import jinja2_template as template, static_file, request
from bottle_flash import FlashPlugin
from bottle import Jinja2Template
from password import *
from database import *
import initialise


import mailing
# import <directory>.<filename>
# Directory must contain an empty __init__.py file
import forms.registration_form as registration_form
import forms.resume_form as resume_form
import forms.login_form as login_form
import forms.news_form as news_form

# app = bottle.Bottle()

STATIC = ROOT + '/static'
RESUMES = STATIC + '/resumes'
BEDRIJVENDAGBOEK = ROOT + '/bedrijvendagboek'

session_opts = {
    'session.type': 'file',
    'session.data_dir': './session/',
    'session.cookie_expires': 1800,
    'session.auto': True,
}

app = beaker.middleware.SessionMiddleware(bottle.app(), session_opts)

message_flash = FlashPlugin(key='messages', secret=secret_key)
Jinja2Template.defaults["get_flashed_messages"] = message_flash.get_flashed_messages
Jinja2Template.settings["extensions"] = ["jinja2.ext.with_"]
initialise.initialise()


@bottle.hook('before_request')
def setup_session():
    request.session = bottle.request.environ.get('beaker.session')


@bottle.get('/favicon.ico')
def get_favicon():
    return None


@bottle.route('/')
def index():
    """returns static template index"""
    return template('static/templates/index_inherit.html', edition=edition,
                    name=request.session.get('logged_in'), date=date_full,
                    admin=(True if request.session.get('logged_in') in admin_users.values() else False))


@bottle.route('/about')
def about():
    """Returns the about page"""
    return template('static/templates/about_inherit.html', edition=edition, name=request.session.get('logged_in'),
                    admin=(True if request.session.get('logged_in') in admin_users.values() else False))


@bottle.route('/contact')
def contact():
    return template('static/templates/contact_inherit.html', edition=edition, name=request.session.get('logged_in'),
                    admin=(True if request.session.get('logged_in') in admin_users.values() else False))


@bottle.route('/student')
def student():
    """Returns the student page"""
    form = resume_form.resume_form()

    return template('static/templates/student_inherit.html', form=form, edition=edition,
                    name=request.session.get('logged_in'),
                    admin=(True if request.session.get('logged_in') in admin_users.values() else False))


@bottle.route('/student', method="post")
def resume_upload():
    """Uploading of the resume
    alle parameters are checked on server side
    resume gets stored in the directory of uploaders
    field of study
    """

    form = resume_form.resume_form(request.POST)

    if form.validate():
        resume.upload(form.field_of_study.data, form.enrollment_number.data, form.resume.data.file.read())
        message_flash.flash('Thank you for uploading your resume', 'success')
        bottle.redirect('/student')
    else:
        for field_name in form.errors:
            for error in form.errors[field_name]:
                message_flash.flash(error, 'danger')
        bottle.redirect('/student')


@bottle.route('/participants')
def participants():
    """retuns all the participating companies (after signed contract has been received)"""
    result = get_all_confirmed_participants(edition)
    return template('static/templates/participants_inherit.html', participants=result, edition=edition,
                    name=request.session.get('logged_in'),
                    admin=(True if request.session.get('logged_in') in admin_users.values() else False))


@bottle.route('/static/<filepath:path>')
def server_static(filepath):
    """routing to static files: css, javascript, should really be done by a webserver (nginx/apache)"""
    return static_file(filepath, root=STATIC)


@bottle.route('/logos/<filepath:path>')
def server_log(filepath):
    """routing to logos, should really be done by a webserver (nginx/apache)"""
    return static_file(filepath, root=STATIC)


@bottle.route('/bedrijvendagboek/<filepath:path>')
def server_log(filepath):
    """routing to company pages"""

    name = request.session.get('logged_in')

    if name is None:
        bottle.redirect('/unauthorized')
    elif name in filepath:
        return static_file(filepath, root=BEDRIJVENDAGBOEK)
    else:
        bottle.redirect('/unauthorized')


@bottle.route('/register')
def register_form():
    """returns the static register form"""

    form = registration_form.RegistrationForm()
    #form.content('class="form-control"')

    return template('static/templates/register_inherit.html', edition=edition, form=form,
                    name=request.session.get('logged_in'),
                    admin=(True if request.session.get('logged_in') in admin_users.values() else False))


@bottle.route('company/<name>/resume')
@bottle.route('/company/<name>')
def company_page(name):
    """routing to company's page where they can view it's information"""

    if request.session.get('logged_in') == name:
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

        return template('static/templates/company_page_inherit.html',
                        address=address, postal=postal,
                        place=place, website=website, tav=tav,
                        tel=tel, fax=fax, email=email, cell=cell,
                        edition=edition, logo=logo, country=country, name=request.session.get('logged_in'),
                        admin=(True if request.session.get('logged_in') in admin_users.values() else False))
    else:
        bottle.redirect('/unauthorized')


@bottle.route('/company/<name>/edit')
def company_page(name):
    """routing to company's page where he can edit it's information"""

    if request.session.get('logged_in') == name:
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

        return template('static/templates/company_page_edit_inherit.html',
                        address=address, postal=postal,
                        place=place, website=website, tav=tav,
                        tel=tel, fax=fax, email=email, cell=cell,
                        edition=edition, logo=logo, country=country, name=request.session.get('logged_in'),
                        admin=(True if request.session.get('logged_in') in admin_users.values() else False))
    else:
        bottle.redirect('/unauthorized')


@bottle.route('/company/<name>/logout')
def logout(name):
    """ends the company's session"""

    try:
        request.session.delete()
        bottle.redirect('/login')
    except KeyError:
        bottle.redirect('/unauthorized')


@bottle.route('/company/<name>/companiesbook')
def companiesbook(name):
    """returns the companies book form"""

    company_template_page = None
    pages = number_of_pages(name, edition) + 1

    page_links = {}

    for index in range(pages):
        if has_free_page(name, index):
            page_links[index] = local_path_free_page(name, index)
        else:
            page_links[index] = None

    if has_page(name):
        company_template_page = local_path(name)

    if request.session.get('logged_in') == name:
        return template('static/templates/companiesbook_inherit.html', edition=edition,
                        company_page=company_template_page, pages=pages, page_links=page_links,
                        name=request.session.get('logged_in'),
                        admin=(True if request.session.get('logged_in') in admin_users.values() else False))
    else:
        bottle.redirect('/unauthorized')


@bottle.route('/company/<name>/companiesbook', method='post')
def static_company_page(name):
    """Fetches the data from the form
    uses this to create his page"""

    if request.session.get('logged_in') == name:
        location = request.forms.get('location')
        if location is not None:
            location = location.decode('UTF-8')
        slogan = request.forms.get('slogan')
        if slogan is not None:
            slogan = slogan.decode('UTF-8')
        why = request.forms.get('why')
        if why is not None:
            why = why.decode('UTF-8')
        field = request.forms.get('schooling')
        if field is not None:
            field = field.decode('UTF-8')
        develop = request.forms.get('develop')
        if develop is not None:
            develop = develop.decode('UTF-8')
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

        create_tex_file(name, location, slogan, why, NL, ENG, FR, DE, JOBS, STAGE, SJOBS, field, develop, FY, CH, WI,
                        BIO, CW, BIN, GEO)
        bottle.redirect('''/company/%s/companiesbook''' % name)
    else:
        bottle.redirect('/unauthorized')

    bottle.redirect('''/company/%s/companiesbook''' % name)


@bottle.route('/company/<name>/logo', method='post')
def upload(name):
    """Fetches the logo send by the company
    and stores it resizes it and saves both
    resized and original folder"""

    if request.session.get('logged_in') == name:
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
    """update given column of given company"""

    if request.session.get('logged_in') == name:
        value = request.forms.get('value').encode('utf8')
        update(name, value, column)
        bottle.redirect('/company/%s' % name)
    else:
        bottle.redirect('/unauthorized')


@bottle.route('/enlist')
def enlist_redirect():
    company = request.session.get('logged_in')
    if company:
        bottle.redirect('/company/%s/enlist' % company)
    bottle.redirect('/login')


@bottle.route('/company/<name>/enlist')
def enlist_form_route(name):
    """returns the enlist form"""

    if request.session.get('logged_in') == name:
        participating = is_participant(name, edition)
        state = None
        stateID = None
        formulaID = None
        formula = None
        tables = None
        promo = None
        remarks = None
        pages = None
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
            pages = participant[8]
            high = participant[7]

            if pages is None:
                pages = 0

        return template('static/templates/enlist_inherit.html', options=get_formulas(),
                        participant=participating,
                        state=state,
                        stateID=stateID,
                        formula=formula,
                        formulaID=formulaID,
                        confirmed=requested_contract(name),
                        tables=tables,
                        promo=promo,
                        pages=pages,
                        remarks=remarks,
                        high=high,
                        edition=edition, name=request.session.get('logged_in'),
                        admin=(True if request.session.get('logged_in') in admin_users.values() else False))
    else:
        bottle.redirect('/unauthorized')


@bottle.route('/company/<name>/enlist', method='post')
def enlist(name):
    """uses the posted information to make the
    company a participant or to change
    it's settings"""

    if request.session.get('logged_in') == name:
        formula = request.forms.get('formula')
        high = request.forms.get('high')

        if not high == "1":
            high = 0

        if is_participant(name, edition):
            tables = request.forms.get('table')
            promo_wands = request.forms.get('promo_wand')
            remarks = request.forms.get('remarks')
            pages = request.forms.get('pages')
            print pages
            edit_participant(name, edition, formula, high, tables, promo_wands, pages, remarks)
        else:
            add_participant(name, edition, formula, high)
        bottle.redirect('/company/%s/enlist' % (name,))
    else:
        bottle.redirect('/unauthorized')


@bottle.route('/company/<name>/confirm')
def confirm(name):
    """Confirm the participant settings, request contract"""

    if request.session.get('logged_in') == name:

        state = participant_converter.state_to_id(get_status(name, edition))

        msg = """<p class="lead">You can't request your contract in your current state</p><hr>your current state: %s<br>
        We must first confirm if there is enough place to meet your needs. If you are currently in queue,
        this means we can not satisfy all your needs.<br>
        You will be contacted soon to discuss your options""" % (get_status(name, edition))

        # if subscription confirmed
        if state == 2:
            change_participant_status(name, edition, participant_converter.id_to_state(3))
        else:
            return template('static/templates/error_inherit.html', error=msg, edition=edition,
                            name=request.session.get('logged_in'),
                            admin=(True if request.session.get('logged_in') in admin_users.values() else False))

        bottle.redirect('''/company/%s/enlist''' % (name,))

    else:
        bottle.redirect('/unauthorized')


@bottle.route('/unauthorized')
def unauthorized():
    """retuns the page showing the unauthorized message"""
    return template('static/templates/error_inherit.html', error="You don't have the right permission", edition=edition,
                    name=request.session.get('logged_in'),
                    admin=(True if request.session.get('logged_in') in admin_users.values() else False))


@bottle.route('/register', method='post')
def register():
    """uses the posted information to create a new company"""

    form = registration_form.RegistrationForm(request.POST)

    if form.validate():

        add_company(form.company_name.data, form.address.data, form.postal.data, form.city.data, form.country.data,
                    form.contact.data, form.email.data, form.tel.data, form.fax.data, form.cel.data, form.website.data,
                    encrypt(form.password.data))
        message_flash.flash('Your account has been created.', 'success')
        bottle.redirect('/login')
    else:
        message = ''
        for field_name in form.errors:
            for error in form.errors[field_name]:
                message += '%s </br>' % error
        message_flash.flash(message, 'danger')

        for field in form:
            try:
                field.data = field.data.decode('utf8')
            except AttributeError:
                pass

        return template('static/templates/register_inherit.html', edition=edition, form=form,
                        name=request.session.get('logged_in'),
                        admin=(True if request.session.get('logged_in') in admin_users.values() else False))
        #return form.country.data


@bottle.route('/login')
def login_form_route():
    """shows the login form"""
    form = login_form.login_form()

    return template('static/templates/login_inherit.html', form=form, edition=edition,
                    name=request.session.get('logged_in'),
                    admin=(True if request.session.get('logged_in') in admin_users.values() else False))


@bottle.route('/login', method='post')
def login_():
    """Start a new session"""

    form = login_form.login_form(request.POST)

    if form.validate():
        email = form.company_name.data
        password = form.password.data
        name = get_company_name_by_email(email)

        route_address = '/company/%s'
        route_address = route_address % name

        if name in admin_users:
            route_address = '/' + admin_users[name]

        if login(name, password):

            request.session["logged_in"] = (name if name not in admin_users else admin_users[name])
            bottle.redirect(route_address)
        else:
            message_flash.flash('The email/password combination is incorrect', 'danger')
            return template('static/templates/login_inherit.html', form=form, edition=edition,
                            name=request.session.get('logged_in'),
                            admin=(True if request.session.get('logged_in') in admin_users.values() else False))

    else:
        message = ""
        for field_name in form.errors:
            for error in form.errors[field_name]:
                message += error
                message += '</br>'
        message_flash.flash(message, 'danger')
        bottle.redirect('/login')


@bottle.route('/recover')
def init_recover_password():
    return template('static/templates/init_password_recovery_inherit', edition=edition,
                    name=request.session.get('logged_in'),
                    admin=(True if request.session.get('logged_in') in admin_users.values() else False))


@bottle.route('/recover', method='post')
def post_recover_password():
    active_company = request.forms.get('company')
    email = request.forms.get('email')
    if confirm_email_company_match(active_company, email):
        hash_value = generate_recovery_hash()
        add_password_hash(active_company, hash_value)
        mailing.send_recovery_email(email, hash_value)
        message_flash.flash('Email with further instructions sent', 'success')
        bottle.redirect('/recover')
    else:
        message_flash.flash('No matching company found', 'danger')
        bottle.redirect('/recover')


@bottle.route('/recover/<hash_value>')
def recover_password(hash_value):
    company_ = find_password_hash(hash_value)

    if company_:
        return template('static/templates/password_recovery_inherit.html', edition=edition,
                        name=request.session.get('logged_in'),
                        admin=(True if request.session.get('logged_in') in admin_users.values() else False), hash=hash)
    else:
        bottle.redirect('/unauthorized')


@bottle.route('/recover/<hash_value>', method='post')
def change_password_url(hash_value):
    company_ = find_password_hash(hash_value)

    password = request.forms.get('password')
    hashed_password = encrypt(password)
    retype_password = request.forms.get('password_confirm')
    if not is_equal(hashed_password, retype_password):
        message_flash.flash("Passwords did not match", 'danger')
        bottle.redirect('/recover/%s' % hash)
    elif company_:
        change_password(company_, hashed_password)
        delete_password_hash(hash)
        message_flash.flash("Password changed successfully", 'success')
        bottle.redirect('/login')
    else:
        bottle.redirect('/unauthorized')


@bottle.route('/pricelist')
def pricelist():
    """retuns static template pricelist"""
    return template('static/templates/pricelist_inherit.html', edition=edition, name=request.session.get('logged_in'),
                    admin=(True if request.session.get('logged_in') in admin_users.values() else False))


@bottle.route('/<name>')
def admin_page(name):
    """returns the admin page"""

    if name in admin_users.values() and request.session.get('logged_in') == name:
        bottle.redirect('/%s/participants' % name)
    else:
        bottle.redirect('/unauthorized')


@bottle.route('/<name>/participants')
def admin_participants(name):
    """Show and edit participant information"""

    if name in admin_users.values() and request.session.get('logged_in') == name:
        return template('static/templates/admin_participants.html', edition=edition,
                        participants=get_participants(edition), name=request.session.get('logged_in'),
                        admin=(True if request.session.get('logged_in') in admin_users.values() else False))
    else:
        bottle.redirect('/unauthorized')

@bottle.route('/<name>/financial')
def admin_financials(name):
    """Show the current confirmed revenue stream, as well as potential revenue"""
    if name in admin_users.values() and request.session.get('logged_in') == name:
        overview = get_financial_overview(edition)
        revenue = get_total_potential_revenue(edition)
        return template('static/templates/admin_financial.html', edition=edition, participants=overview,
                        revenue=revenue, name=request.session.get('logged_in'),
                        admin=(True if request.session.get('logged_in') in admin_users.values() else False))
    else:
        bottle.redirect('/unauthorized')


@bottle.route('/<name>/participants/setstate/<company>/<state>')
def set_state(name, company, state):
    """change the state of the company"""

    if name in admin_users.values() and request.session.get('logged_in') == name:
        state = participant_converter.id_to_state(state)

        change_participant_status(company, edition, state)
        bottle.redirect('/%s/participants' % name)
    else:
        bottle.redirect('/unauthorized')


@bottle.route('/company/<name>/resumes')
def show_resumes(name):
    years = get_participating_years(name)
    return template('static/templates/company_resume_inherit.html', years=years, sel_year=0, edition=edition,
                    name=request.session.get('logged_in'),
                    admin=(True if request.session.get('logged_in') in admin_users.values() else False))


@bottle.route('/company/<name>/resumes/<sel_year>')
def show_resumes_year(name, sel_year):
    return static_file(sel_year + ".zip", root=RESUMES)


@bottle.route('/company/<name>/upload/<index>', method='post')
def upload_free_page(name, index):
    if request.session.get('logged_in') == name:

        page = request.files.free_page
        if page is None:
            bottle.redirect('''/company/%s/companiesbook''' % (name,))
        if not (page.filename.lower().endswith('.pdf')):
            message_flash.flash('File must be a pdf', 'danger')
            bottle.redirect('''/company/%s/companiesbook''' % (name,))

        raw = request.files.free_page.file.read()

        free_page_upload(name, index, raw)
        bottle.redirect('''/company/%s/companiesbook''' % (name,))
    else:
        bottle.redirect('/unauthorized')
