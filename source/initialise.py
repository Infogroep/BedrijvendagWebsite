import os
import database
from config import *


def initialise():
	try:
		initialise_field_folders()
	except:
		print "field files creation failed"
	try:
		initialise_database()
	except:
		print "database creation failed"

def  initialise_field_folders():

	if (not(os.path.exists(ROOT + "/" + field_directory))):
		os.mkdir(ROOT + "/" + field_directory)
	
	for field in fields_of_study:
		
		direcory_name = ROOT + "/" + field_directory + "/" + field[0]

		if (not (os.path.exists(direcory_name))):
			os.mkdir(direcory_name)

def initialise_database():
	
	if (not (os.path.exists(database_name))):
		database.db_initialise()
