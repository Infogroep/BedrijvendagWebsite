import sqlite3
import time

# Opens the connection to the website data.
# This different from the companies data
def open_connection():
    return sqlite3.connect('website-data.db')

# Closes the connection
# First commits the changes
def close_connection(connection):
    connection.commit()
    connection.close()

def initialise():
    connection = open_connection()
    cursor = connection.cursor()
    
    cursor.execute('''CREATE TABLE Newsfeed (Date DATA, Description CHAR(255), Newsmessage TEXT)''')
    
    close_connection(connection)

def get_news_feed():
    connection = open_connection()
    cursor = connection.cursor()

    cursor.execute('''SELECT * FROM Newsfeed ORDER BY Date DESC''')
    
    queryresult = cursor.fetchall()
    
    close_connection(connection)
    return queryresult


