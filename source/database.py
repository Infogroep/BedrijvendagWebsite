import sqlite3
import initialise, participant_converter
from password import *
from participant_state import *
from config import database_name
import MySQLdb as mysql
import time, datetime


# Opens the connection to the website data.
# This different from the companies data
def open_connection():
    '''Opens connection to the website database'''
    return sqlite3.connect(database_name)

def open_companies_connection():
    '''Opens connection to the companies database'''
    return mysql.connect('127.0.0.1', 'bedrijvendag', 'groenwater', 'bedrijvendagDEV')

# Closes the connection
# First commits the changes
def close_connection(connection):
    '''Commits any changes and closes the connection to any database'''
    connection.commit()
    connection.close()


# Creates the database
# sqlite database for non-company, information
def db_initialise():
    '''Initialises the website database'''
    connection = open_connection()
    cursor = connection.cursor()
    
    cursor.execute('''CREATE TABLE Newsfeed (ID int, date DATA, description VARCHAR(255), newsmessage TEXT)''')
    cursor.execute('''CREATE TABLE Companies (name VARCHAR(255), key VARCHAR(255))''')
    cursor.execute('''CREATE TABLE Logos (name VARCHAR(255), filename VARCHAR(255))''')
    cursor.execute('''CREATE TABLE Financial (date, DATA, kring VARCHAR(30), description VARCHAR(255), amount INT, paid BIT, refunded BIT''')
    
    close_connection(connection)

def get_new_news_id():
    '''Generates a new id for a newsitem in the newsfeed'''

    connection = open_connection()
    cursor = connection.cursor()
    
    query = '''SELECT MAX(id) FROM Newsfeed'''
    
    result = cursor.fetchone()
    
    close_connection(connection)
    try:
        return result[0] + 1
    except:
        return 0

def get_website(name):
    '''Returns the website from given company. Company name is expected to be a string'''

    connection = open_companies_connection()
    cursor = connection.cursor()
    
    cursor.execute('''SELECT website FROM companies WHERE name = %s''', name)

    result = cursor.fetchone()
    
    try:
        return result[0]
    except:
        return ""

# extracts the newsfeed from the sqlite databse
# time is an unix timestamp, we first convert to an human readable time
def get_news_feed():
    '''Fetches all the news items currently in the newsfeed 
    remark: maybe fetch only the 10 newest?'''

    connection = open_connection()
    cursor = connection.cursor()

    cursor.execute('''SELECT * FROM Newsfeed ORDER BY Date DESC''')
    
    queryresult = cursor.fetchall()
    
    close_connection(connection)
    
    #queryresult is a tuple of tuples. you can't write to tuples thus we first map them to list
    queryresult = map(list, queryresult)
    
    # converting to human readable time
    # I know it's not part of the database abstraction I'm so very sorry
    # You can always rewrite it.
    for result in queryresult:
        date = datetime.datetime.fromtimestamp(result[1])
        result[1] = date.strftime("%d %B %Y - %H:%M")
    
    return queryresult

def set_logo(company, filename):
    '''set the path to the logo in the database'''
    connection = open_connection()
    cursor = connection.cursor()
    
    if get_logo(company):
        cursor.execute('''UPDATE Logos SET Filename = ? WHERE name = ?''', (filename, company))
    else:
        cursor.execute('''INSERT INTO Logos VALUES(?, ?)''', (company, filename))
    close_connection(connection)

def get_logo(company):
    '''Get the path to the companies logo'''
    connection = open_connection()
    cursor = connection.cursor()
    
    query = '''SELECT Filename FROM Logos WHERE name = "%s"''' % (company,)
    cursor.execute(query)
    
    queryresult = cursor.fetchall()
    
    close_connection(connection)
    
    if(len(queryresult) == 0):
        return False
    else:
        result = queryresult[0][0]
        return result

def company(name):
    '''Get all the data stored in the database of this company'''
    connection = open_companies_connection()
    cursor = connection.cursor()
    
    cursor.execute('''SELECT id, name, address, area_code, place, country, tav, email, telephone_number, fax_number, cellphone_number, website FROM companies WHERE name = "%s"''' % name)
    
    queryresult = cursor.fetchall()
    
   
    close_connection(connection)
    if (len(queryresult) == 1):
        return queryresult[0]
    else:
        return False

def add_login(user, password):
    '''saves a login, password pair in the database.
    Password is already encrypted before it gets here'''
    
    connection = open_connection()
    cursor = connection.cursor()
    
#    cursor.execute(query)
    cursor.execute('''INSERT INTO Companies VALUES(?, ?)''', (user, password))
    
    close_connection(connection)

def login(user, password):
    '''returns true if the user password pair matches
    false otherwise'''
    connection = open_connection()
    cursor = connection.cursor()
    
    cursor.execute('''SELECT key from Companies where name=?''', (user,))
    
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

def get_new_company_id():
    '''Generates a new company id'''
    connection = open_companies_connection()
    cursor = connection.cursor()
    
    query = '''SELECT MAX(id) FROM companies'''
    
    cursor.execute(query)
    
    result = cursor.fetchone()
    
    close_connection(connection)
    try:
        return result[0] + 1
    except:
        return 0


def add_company(name, address, postal, place, country, tav, email, tel, fax, cell, website):
    '''add a company to the company database'''

    connection = open_companies_connection()
    cursor = connection.cursor()
    
    ID = get_new_company_id()
    
    # The module to work with MySQL doesn't support ? string parsing when executing queries
    cursor.execute('''INSERT INTO companies VALUES(%s, "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "")''' % \
                  (ID, name, address, postal, place, country, tav, email, tel, fax, cell, website))

    close_connection(connection)

def add_news_item(short, text):
    '''Add a news item. News item are displayed on the front page'''

    connection = open_connection()
    cursor = connection.cursor()
    
    ID = get_new_news_id()
    now = time.time()
    
    cursor.execute('''INSERT INTO Newsfeed VALUES(?, ?, ?, ?)''', (ID, now, short, text))
    
    close_connection(connection)

def get_companyID(name):
    '''Get the id of given company'''
    connection = open_companies_connection()
    cursor = connection.cursor()
    
    cursor.execute('''SELECT ID FROM companies where name = "%s"''' % (name,))
    
    result = cursor.fetchone()
    
    ID = result[0]

    return ID

def is_participant(name, year):
    '''Checks if given company is/was a participant at given year'''
    connection = open_companies_connection()
    cursor = connection.cursor()
    
    ID = get_companyID(name)
    
    cursor.execute('''SELECT companyID FROM participants where companyID = "%s" and year = "%s"''' % (ID, year))

    result = cursor.fetchall()
    close_connection(connection)

    if (len(result) == 0):
        return False
    else:
        return True

def get_status(name, edition):
    '''Gets the current status of the participant.
    if it isn't a participant return None'''
    if(is_participant(name, edition)):
        connection = open_companies_connection()
        cursor = connection.cursor()

        ID = get_companyID(name)
        cursor.execute('''SELECT state FROM participants WHERE companyID= %s and year = "%s" ''' % (ID, edition))

        result = cursor.fetchone()

        close_connection(connection)
        return result[0]



def get_formulas():
    '''fetches all possible formulas'''
    connection = open_companies_connection()
    cursor = connection.cursor()
    
    cursor.execute('''SELECT ID, name, price FROM formula''')
    close_connection(connection)
    
    return cursor.fetchall()

def update(company, value, column):
    '''Updates given column of given company to given value'''
    connection = open_companies_connection()
    cursor = connection.cursor()
    
    cursor.execute('''UPDATE companies SET %s = "%s" where name = "%s"''' % (column, value, company))
    
    close_connection(connection)

def add_participant(company, year, formula, high):
    '''add a participant to the given edition with given formula and high flag
    company is also given. Checks if company isn't a participant yet '''

    connection = open_companies_connection()
    cursor = connection.cursor()

    if(is_participant(company, year)):
        return False

    ID = get_companyID(company)
    state = participant_converter.id_to_state(0)

    

    tables = 2
    promotion_wands = 2

    if((formula == 2) or (formula == 3)):
        tables = 0
        promotion_wands = 0

    cursor.execute('''INSERT INTO participants VALUES (%s, %s, %s, "%s", %s, %s, "", %s)''' % (ID, year, formula, state, tables, promotion_wands, high))
    close_connection(connection)

def get_participant(company_id, year):
    '''get participant information of given company of given year'''
    connection = open_companies_connection()
    cursor = connection.cursor()    

    cursor.execute('''SELECT * FROM participants WHERE companyID = %s AND year = %s''' % (company_id, year))

    res = cursor.fetchone()
    close_connection(connection)

    return res


def edit_participant(company, year, formula, high, tables, promotion_wands, remarks):
    '''edit the participant information'''
    ID = get_companyID(company)
    participant_information = get_participant(ID, year)

    current_formula = participant_information[2]
    state = participant_information[3]
    current_high = participant_information[7]

    formula = int(formula)

    if ((current_high != high) or (current_formula != formula)):
        print "different"
        state = participant_converter.id_to_state(0)

    if formula == 1:
        tables = 2
        promotion_wands = 2
    elif ((formula == 2) or (formula ==3)):
        tables = promotion_wands = 0

    if tables is None:
        tables = 2
    if promotion_wands is None:
        promotion_wands = 2


    connection = open_companies_connection()
    cursor = connection.cursor()

    cursor.execute('''UPDATE participants SET formulaID = %s, state = "%s", tables = %s, promotion_wands = %s, high_stand = %s, remarks = "%s" WHERE companyID = %s''' % \
                      (formula, state, tables, promotion_wands, high, remarks, ID))

    close_connection(connection)

def get_company_name_by_id(company_id):
    '''get the name of the company by given id'''
    connection = open_companies_connection()
    cursor = connection.cursor()

    cursor.execute('''SELECT name FROM companies WHERE ID = %s''' % (company_id,))

    result = cursor.fetchone()
    close_connection(connection)
    return result[0]

def get_participants(year):
    '''Get all participants of a given year'''

    connection = open_companies_connection()
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

    connection = open_companies_connection()
    cursor = connection.cursor()

    cursor.execute('''UPDATE participants SET state = "%s" where companyID = %s AND year = %s''' % (state, ID, year))

    close_connection(connection)    


def get_formula_by_id(id):
    '''get the formula by given id'''
    connection = open_companies_connection()
    cursor = connection.cursor()

    cursor.execute('''SELECT name FROM formula where ID = %s''' %(id))

    result = cursor.fetchone()

    close_connection(connection)

    return result[0]

def get_formula(name, edition):
    '''Get the formula of a given company and year'''
    connection = open_companies_connection()
    cursor = connection.cursor()

    ID = get_companyID(name)

    cursor.execute('''SELECT formulaID FROM participants where companyID = %s and year = %s''' % (ID, edition))

    result = cursor.fetchone()

    close_connection(connection)

    return result[0]

