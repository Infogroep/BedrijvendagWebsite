import os
import database
from config import *


def initialise():
	'''Calls all the initialise functions and check wether the were succesfull or not'''
	try:
		initialise_field_folders()
	except:
		print "field files creation failed"

	try:
		initialise_logo_folders()
	except:
		print "logo folders creation failed"

	try:
		initialise_database()
	except:
		print "database creation failed"

def  initialise_field_folders():
	'''Creates the folders per field to collect the resumes is.
	First checks wether or not the folders already exists
	Fields are located in config.py (fields_of_study)'''

	if (not(os.path.exists(ROOT + "/" + field_directory))):
		os.mkdir(ROOT + "/" + field_directory)

	if (not(os.path.exists(ROOT + "/" + field_directory + "/" + edition))):
		os.mkdir(ROOT + "/" + field_directory + "/" + edition)
	
	for field in fields_of_study:
		
		direcory_name = ROOT + "/" + field_directory + "/" + edition + "/" + field[0]

		if (not (os.path.exists(direcory_name))):
			os.mkdir(direcory_name)

def initialise_database():
	'''Calls the the initialise functions from databse.py if the database does not yet exist'''
	
	if (not (os.path.exists(database_name))):
		database.db_initialise()

def initialise_logo_folders():
	'''Creates the folders where the company logos are to be stored
	folder names are locate in config.py'''
	if (not (os.path.exists(logo_original))):
		os.mkdir(logo_original)

	if(not(os.path.exists(logo_resized))):
		os.mkdir(logo_resized)

