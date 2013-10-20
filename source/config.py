import os

file_name = os.path.abspath(__file__)

ROOT = os.path.dirname(file_name)
field_directory = "resumes"

date = "19/03/2014"
event_location = "Nelson Mandela"

event_start_time = "11:00"
event_stop_time = "17:00"
event_close_down = "18:00"

logo_original = "static/original"
logo_resized = "static/resized"

edition = "2014"

database_name = "website-data.db"

fields_of_study = (("computerwetenschappen", "computer science"),
				   ("bio-ingenieur", "Bioscience engineering"),
        		   ("fysica", "Physics"),
        		   ("chemie", "Chemistry"),
        		   ("wiskunde", "Mathematics"),
        		   ("biologie", "Biology"),
        		   ("geografie", "Geography"),
        		   ("ander", "Other"),
				  )

participant_states = ((0, "Awaiting confirmation"),
					  (1, "In queue"),
					  (2, "Subcription confirmed"),
					  (3, "Requested contract"),
					  (4, "Contract signed"),
					  (5, "Received payment"),
					  (6, "Annulation")
					 )