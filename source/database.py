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
    return sqlite3.connect(database_name)

def open_companies_connection():
    return mysql.connect('127.0.0.1', 'bedrijvendag', 'groenwater', 'bedrijvendagDEV')

# Closes the connection
# First commits the changes
def close_connection(connection):
    connection.commit()
    connection.close()


# Creates the database
# sqlite database for non-company, information
def db_initialise():
    connection = open_connection()
    cursor = connection.cursor()
    
    cursor.execute('''CREATE TABLE Newsfeed (ID int, date DATA, description VARCHAR(255), newsmessage TEXT)''')
    cursor.execute('''CREATE TABLE Companies (name VARCHAR(255), key VARCHAR(255))''')
    cursor.execute('''CREATE TABLE Logos (name VARCHAR(255), filename VARCHAR(255))''')
    cursor.execute('''CREATE TABLE Financial (date, DATA, kring VARCHAR(30), description VARCHAR(255), amount INT, paid BIT, refunded BIT''')
    
    close_connection(connection)

def get_new_news_id():
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
    connection = open_connection()
    cursor = connection.cursor()
    
    if get_logo(company):
        cursor.execute('''UPDATE Logos SET Filename = ? WHERE name = ?''', (filename, company))
    else:
        cursor.execute('''INSERT INTO Logos VALUES(?, ?)''', (company, filename))
    close_connection(connection)

def get_logo(company):
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
    
    connection = open_connection()
    cursor = connection.cursor()
    
#    cursor.execute(query)
    cursor.execute('''INSERT INTO Companies VALUES(?, ?)''', (user, password))
    
    close_connection(connection)

def login(user, password):
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
        if is_equal(stored, password):
            return True
        else:
            return False

def get_new_company_id():
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
    connection = open_companies_connection()
    cursor = connection.cursor()
    
    ID = get_new_company_id()
    
    # The module to work with MySQL doesn't support ? string parsing when executing queries
    cursor.execute('''INSERT INTO companies VALUES(%s, "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "")''' % \
                  (ID, name, address, postal, place, country, tav, email, tel, fax, cell, website))

    close_connection(connection)

def add_news_item(short, text):
    connection = open_connection()
    cursor = connection.cursor()
    
    ID = get_new_news_id()
    now = time.time()
    
    cursor.execute('''INSERT INTO Newsfeed VALUES(?, ?, ?, ?)''', (ID, now, short, text))
    
    close_connection(connection)

def get_companyID(name):
    connection = open_companies_connection()
    cursor = connection.cursor()
    
    cursor.execute('''SELECT ID FROM companies where name = "%s"''' % (name,))
    
    result = cursor.fetchone()
    
    ID = result[0]

    return ID

def is_participant(name, year):
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
    if(is_participant(name, edition)):
        connection = open_companies_connection()
        cursor = connection.cursor()

        ID = get_companyID(name)
        cursor.execute('''SELECT state FROM participants WHERE companyID= %s and year = "%s" ''' % (ID, edition))

        result = cursor.fetchone()

        close_connection(connection)
        return result[0]


def get_formulas():
    connection = open_companies_connection()
    cursor = connection.cursor()
    
    cursor.execute('''SELECT ID, name, price FROM formula''')
    close_connection(connection)
    
    return cursor.fetchall()

def update(company, value, column):
    connection = open_companies_connection()
    cursor = connection.cursor()
    
    cursor.execute('''UPDATE companies SET %s = "%s" where name = "%s"''' % (column, value, company))
    
    close_connection(connection)

def add_participant(company, year, formula, high):
    connection = open_companies_connection()
    cursor = connection.cursor()

    if(is_participant(company, year)):
        return

    ID = get_companyID(company)
    state = participant_converter.id_to_state(0)

    print state

    tables = 2
    promotion_wands = 2

    if((formula == 2) or (formula == 3)):
        tables = 0
        promotion_wands = 0

#    cursor.execute('''INSERT INTO participants VALUES (%s, %s, %s, "%s", %s, %s, "", %s)''' % (ID, year, formula, state, tables, promotion_wands, high))
    cursor.execute('''INSERT INTO participants VALUES (%s, %s, %s, "%s", %s, %s, "", %s)''' % (ID, year, formula, state, tables, promotion_wands, high))
    close_connection(connection)

def get_company_name_by_id(company_id):
    connection = open_companies_connection()
    cursor = connection.cursor()

    cursor.execute('''SELECT name FROM companies WHERE ID = %s''' % (company_id,))

    result = cursor.fetchone()
    close_connection(connection)
    return result[0]

def get_participants(year):
    connection = open_companies_connection()
    cursor = connection.cursor()

    cursor.execute('''SELECT companyID, formulaID, state, tables, high_stand, remarks FROM participants where year = %s''' % (year,))

    result = cursor.fetchall()
    close_connection(connection)

    result = map(list, result)
    
    # converting to human readable time
    # I know it's not part of the database abstraction I'm so very sorry
    # You can always rewrite it.
    for res in result:
        company_name = get_company_name_by_id(res[0])
        res[0] = company_name
        high = res[4]

        if high:
            res[4] = 1

    return result

def change_participant_status(company, year, state):

    ID = get_companyID(company)

    connection = open_companies_connection()
    cursor = connection.cursor()

    cursor.execute('''UPDATE participants SET state = %s where companyID = %s AND year = %s''' % (state, ID, year))

    close_connection(connection)    


def get_formula_by_id(id):
    connection = open_companies_connection()
    cursor = connection.cursor()

    cursor.execute('''SELECT name FROM formula where ID = %s''' %(id))

    close_connection(connection)