import sqlite3
import initialise, participant_converter
from password import *
from participant_state import *
from config import database_name, database_user, database_password, database_host
import MySQLdb as mysql
import time, datetime, mailing


# Opens the connection to the website data.
# This different from the companies data

def open_connection():
    '''Opens connection to the companies database'''
    return mysql.connect(database_host, database_user, database_password, database_name, charset='utf8')

# Closes the connection
# First commits the changes
def close_connection(connection):
    '''Commits any changes and closes the connection to any database'''
    connection.commit()
    connection.close()

def get_website(name):
    '''Returns the website from given company. Company name is expected to be a string'''

    connection = open_connection()
    cursor = connection.cursor()
    
    cursor.execute('''SELECT website FROM companies WHERE name = "%s"''', name)

    result = cursor.fetchone()
    
    try:
        return result[0]
    except:
        return ""

# extracts the newsfeed from the databse
# time is an unix timestamp, we first convert to an human readable time
def get_news_feed():
    '''Fetches all the news items currently in the newsfeed 
    remark: maybe fetch only the 10 newest?'''

    connection = open_connection()
    cursor = connection.cursor()

    cursor.execute('''SELECT * FROM newsfeed ORDER BY postdate DESC''')
    
    queryresult = cursor.fetchall()
    
    close_connection(connection)
    
    #queryresult is a tuple of tuples. you can't write to tuples thus we first map them to list
    queryresult = map(list, queryresult)
    
    # converting to human readable time
    # I know it's not part of the database abstraction I'm so very sorry
    # You can always rewrite it.
    for result in queryresult:
        date = datetime.datetime.fromtimestamp(float(result[1]))
        result[1] = date.strftime("%d %B %Y - %H:%M")
    
    return queryresult

def get_logo(company):
    '''Get the path to the companies logo'''
    connection = open_connection()
    cursor = connection.cursor()
    
    query = '''SELECT filename FROM companies WHERE name = "%s"''' % (company,)
    cursor.execute(query)
    
    queryresult = cursor.fetchall()
    
    close_connection(connection)
    
    if(len(queryresult) == 0):
        return False
    else:
        result = queryresult[0][0]
        return result

def set_logo(company, filename):
    '''set the path to the logo in the database'''
    connection = open_connection()
    cursor = connection.cursor()

    cursor.execute('''UPDATE companies SET filename = "%s" WHERE name = "%s"''' % (filename, company))

    close_connection(connection)


def company(name):
    '''Get all the data stored in the database of this company'''
    connection = open_connection()
    cursor = connection.cursor()
    
    cursor.execute('''SELECT id, name, address, area_code, place, country, tav, email, telephone_number, fax_number, cellphone_number, website FROM companies WHERE name = "%s"''' % name)
    
    queryresult = cursor.fetchall()
    
   
    close_connection(connection)
    if (len(queryresult) == 1):
        return queryresult[0]
    else:
        return False

def login(user, password):
    '''returns true if the user password pair matches
    false otherwise'''
    connection = open_connection()
    cursor = connection.cursor()
    
    cursor.execute('''SELECT password from companies where name="%s"''' % user)
    
    result = cursor.fetchone()
#    company_ = company(user)

#    if not(company_):
#        return False
    if result is None:
        return False
    elif(len(result) == 0):
        return False
    else:
        stored = result[0]
        if is_equal(stored.encode('utf-8'), password):
            return True
        else:
            return False

def add_company(name, address, postal, place, country, tav, email, tel, fax, cell, website, hashed_password):
    '''add a company to the company database'''

    connection = open_connection()
    cursor = connection.cursor()
        
    # The module to work with MySQL doesn't support ? string parsing when executing queries
    cursor.execute('''INSERT INTO companies (name, address, area_code, place, country, tav, email, telephone_number, fax_number, cellphone_number, website, password) VALUES("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")''' % \
                  (name, address, postal, place, country, tav, email, tel, fax, cell, website, hashed_password))

    close_connection(connection)

def add_news_item(short, text):
    '''Add a news item. News item are displayed on the front page'''

    connection = open_connection()
    cursor = connection.cursor()

    now = time.time()
    
    cursor.execute('''INSERT INTO newsfeed (postdate, description, newsmessage) VALUES(%s, "%s", "%s")''' % (now, short, text))
    
    close_connection(connection)

def get_companyID(name):
    '''Get the id of given company'''
    connection = open_connection()
    cursor = connection.cursor()
    
    cursor.execute('''SELECT ID FROM companies where name = "%s"''' % (name,))
    
    result = cursor.fetchone()
    
    ID = result[0]

    return ID

def is_participant(name, year):
    '''Checks if given company is/was a participant at given year'''
    connection = open_connection()
    cursor = connection.cursor()
    
    ID = get_companyID(name)
    
    cursor.execute('''SELECT companyID FROM participants where companyID = "%s" and year = "%s"''' % (ID, year))

    result = cursor.fetchall()
    close_connection(connection)

    if (len(result) == 0):
        return False
    else:
        return True

def get_all_participants(year):
    '''gets all participants and their corresponding logos'''
    connection = open_connection()
    cursor = connection.cursor()
    cursor.execute('''SELECT c.filename,c.name, c.website FROM companies c,participants p WHERE c.id=p.companyID AND year = %s''' % (year))
    queryresult = cursor.fetchall()
    close_connection(connection)
    
    if(len(queryresult) == 0):
        return []
    else:
        return queryresult

def get_status(name, edition):
    '''Gets the current status of the participant.
    if it isn't a participant return None'''
    if(is_participant(name, edition)):
        connection = open_connection()
        cursor = connection.cursor()

        ID = get_companyID(name)
        cursor.execute('''SELECT state FROM participants WHERE companyID= %s and year = "%s" ''' % (ID, edition))

        result = cursor.fetchone()

        close_connection(connection)
        return result[0]



def get_formulas():
    '''fetches all possible formulas'''
    connection = open_connection()
    cursor = connection.cursor()
    
    cursor.execute('''SELECT ID, name, price FROM formula''')
    close_connection(connection)
    
    return cursor.fetchall()

def update(company, value, column):
    '''Updates given column of given company to given value'''
    connection = open_connection()
    cursor = connection.cursor()
    
    cursor.execute('''UPDATE companies SET %s = "%s" where name = "%s"''' % (column, value, company))
    
    close_connection(connection)

def add_participant(company, year, formula, high):
    '''add a participant to the given edition with given formula and high flag
    company is also given. Checks if company isn't a participant yet '''

    if(is_participant(company, year)):
        return False

    ID = get_companyID(company)
    state = participant_converter.id_to_state(0)

    tables = 2
    promotion_wands = 2
    number_of_pages = 0
    remarks = ""

    if((formula == 2) or (formula == 3)):
        tables = 0
        promotion_wands = 0

    connection = open_connection()
    cursor = connection.cursor()

    cursor.execute('''INSERT INTO participants (companyID, year, formulaID, state, tables, promotion_wand, high_stand, number_of_pages, remarks) VALUES \
                                               (%s, %s, %s, "%s", %s, %s, %s, %s, "%s")''' % \
                                               (ID, year, formula, state, tables, promotion_wands, high, number_of_pages, remarks))
    close_connection(connection)

    mailing.send_enlist_mail(company)

    

def get_participant(company_id, year):
    '''get participant information of given company of given year'''
    connection = open_connection()
    cursor = connection.cursor()    

    cursor.execute('''SELECT * FROM participants WHERE companyID = %s AND year = %s''' % (company_id, year))

    res = cursor.fetchone()
    close_connection(connection)

    return res


def edit_participant(company, year, formula, high, tables, promotion_wands, pages, remarks):
    '''edit the participant information'''
    ID = get_companyID(company)
    participant_information = get_participant(ID, year)

    current_formula = participant_information[2]
    state = participant_information[3]
    current_high = participant_information[7]

    formula = int(formula)

    if (((int(current_high) != int(high)) and int(high) == 1) or (current_formula != formula)):
        print "different"
        state = participant_converter.id_to_state(0)

    if formula == 2:
        tables = 2
        promotion_wands = 2
    elif ((formula == 3) or (formula == 4)):
        tables = promotion_wands = 0

    ## Rounds to the nearest 0,5
    pages = float(pages)
    pages = round(pages * 20, -1) /20

    if tables is None:
        tables = 2
    if promotion_wands is None:
        promotion_wands = 2
    if remarks is None:
        remarks = ""


    connection = open_connection()
    cursor = connection.cursor()

    cursor.execute('''UPDATE participants SET formulaID = %s, state = "%s", tables = %s, promotion_wand = %s, high_stand = %s, number_of_pages = %s, remarks = "%s" WHERE companyID = %s''' % \
                      (formula, state, tables, promotion_wands, high, pages, remarks, ID))

    close_connection(connection)

def get_company_name_by_id(company_id):
    '''get the name of the company by given id'''
    connection = open_connection()
    cursor = connection.cursor()

    cursor.execute('''SELECT name FROM companies WHERE ID = %s''' % (company_id,))

    result = cursor.fetchone()
    close_connection(connection)
    return result[0]

def get_participants(year):
    '''Get all participants of a given year'''

    connection = open_connection()
    cursor = connection.cursor()

    cursor.execute('''SELECT companyID, formulaID, state, tables, promotion_wand, high_stand, remarks FROM participants where year = %s''' % (year,))

    result = cursor.fetchall()
    close_connection(connection)

    result = map(lambda t: t + ("",), result)

    result = map(list, result)
    
    # converting to human readable time
    # I know it's not part of the database abstraction I'm so very sorry
    # You can always rewrite it.
    for res in result:
        company_name = get_company_name_by_id(res[0])
        res[0] = company_name


        formula = get_formula_by_id(res[1])
        res[1] = formula

        stateID = participant_converter.state_to_id(res[2])
        res[7] = stateID

        high = res[4]

        if high:
            res[4] = 1

    return result

def change_participant_status(company, year, state):
    '''Changes the status of the given participant (company and year)'''

    ID = get_companyID(company)

    connection = open_connection()
    cursor = connection.cursor()

    cursor.execute('''UPDATE participants SET state = "%s" where companyID = %s AND year = %s''' % (state, ID, year))

    cursor.execute('''SELECT email from companies where ID = %s''' % (ID,))
    result = cursor.fetchone()

    close_connection(connection)

    print result, state

    if (participant_converter.state_to_id(state) == 2):
        mailing.send_confirmation_mail(result[0])


def get_formula_by_id(id):
    '''get the formula by given id'''
    connection = open_connection()
    cursor = connection.cursor()

    cursor.execute('''SELECT name FROM formula where ID = %s''' %(id))

    result = cursor.fetchone()

    close_connection(connection)

    return result[0]

def get_formula(name, edition):
    '''Get the formula of a given company and year'''
    connection = open_connection()
    cursor = connection.cursor()

    ID = get_companyID(name)

    cursor.execute('''SELECT formulaID FROM participants where companyID = %s and year = %s''' % (ID, edition))

    result = cursor.fetchone()

    close_connection(connection)

    return result[0]

def get_formula_default_pages(id):
    '''Get the number of pages included in this formula'''

    connection = open_connection()
    cursor = connection.cursor()

    cursor.execute('''SELECT number_of_pages from formula where ID = %s''' %(id))

    result = cursor.fetchone()

    close_connection(connection)

    return result[0]

def remove_news_item(news_id):
    '''Removes a news item by id'''

    connection = open_connection()
    cursor = connection.cursor()

    cursor.execute('''DELETE FROM newsfeed WHERE newsID = %s''' % (news_id,))

    close_connection(connection)

def confirm_email_company_match(company, email):
    connection = open_connection()
    cursor = connection.cursor()

    cursor.execute('''SELECT companies.ID FROM companies WHERE companies.name = "%s" AND companies.email = "%s"''' % (company, email))

    result = cursor.fetchone()
    close_connection(connection)

    if result:
        return result[0]
    else:
        return False

def find_password_hash(hash):
    connection = open_connection()
    cursor = connection.cursor()

    cursor.execute('''SELECT companies.name FROM recover_password INNER JOIN companies ON recover_password.companyID = companies.ID WHERE password_url = "%s"''' % hash)

    result = cursor.fetchone()

    close_connection(connection)
    
    if result:
        return result[0]
    else:
        return False

def add_password_hash(company, hash):
    connection = open_connection()
    cursor = connection.cursor()

    companyid = get_companyID(company)

    cursor.execute('''INSERT INTO recover_password (companyID, password_url) VALUES (%s, "%s")''' % (companyid, hash))
    close_connection(connection)
    
def delete_password_hash(hash):
    connection = open_connection()
    cursor = connection.cursor()

    cursor.execute('''DELETE FROM recover_password WHERE password_url="%s"''' % hash)

    close_connection(connection)

def change_password(company_name, hashed_password):
    connection = open_connection()
    cursor = connection.cursor()

    cursor.execute('''UPDATE companies SET password = "%s" where name = "%s"''' % (hashed_password, company_name))

    close_connection(connection)


def number_of_pages(company_name, year):
    connection = open_connection()
    cursor = connection.cursor()    

    company_id = get_companyID(company_name)

    cursor.execute('''SELECT number_of_pages FROM participants WHERE companyID = %s AND year = %s''' % (company_id, year))

    result = cursor.fetchone()

    close_connection(connection)

    
    if result:
        return result[0]
    else:
        return -1

def get_participating_years(company_name):
    company_id = get_companyID(company_name)

    connection = open_connection()
    cursor = connection.cursor()

    cursor.execute('''SELECT year FROM participants WHERE companyID = %s''' % (company_id))

    result = list()

    for row in cursor.fetchall():
        result.append(row[0])

    print result
    return result