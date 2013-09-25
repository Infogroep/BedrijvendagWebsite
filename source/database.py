import sqlite3
import MySQLdb as mysql
import time

# Opens the connection to the website data.
# This different from the companies data
def open_connection():
    return sqlite3.connect('website-data.db')

def open_companies_connection():
    return mysql.connect()

# Closes the connection
# First commits the changes
def close_connection(connection):
    connection.commit()
    connection.close()

def initialise():
    connection = open_connection()
    cursor = connection.cursor()
    
    cursor.execute('''CREATE TABLE Newsfeed (Date DATA, Description CHAR(255), Newsmessage TEXT)''')
    cursor.execute('''CREATE TABLE Companies (Name CHAR(255), Key CHAR(255))''')
    
    close_connection(connection)

def get_news_feed():
    connection = open_connection()
    cursor = connection.cursor()

    cursor.execute('''SELECT * FROM Newsfeed ORDER BY Date DESC''')
    
    queryresult = cursor.fetchall()
    
    close_connection(connection)
    return queryresult

def company(name):
    connection = open_companies_connection()
    cursor = connection.cursor()
   
    query = '''SELECT id, name, adres, postcode, place, country, tav, email, telephonenr, faxnr, gsmnr, website FROM companies WHERE name="%s"'''
    query = query % name

     
    cursor.execute(query)
    queryresult = cursor.fetchall()
    
   
    close_connection(connection)
    if (len(queryresult) == 1):
        return queryresult
    else:
        return False

def add_login(user, password):
    query = 'INSERT INTO Companies VALUES("' + user + '", "' + password + '")'
    
    print query
    
    connection = open_connection()
    cursor = connection.cursor()
    
    cursor.execute(query)
    
    close_connection(connection)



