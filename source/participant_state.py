import database, participant_converter
from config import edition, participant_states

def get_state_ID(company):
	'''Get the id of the state where the company is currently in'''
	return participant_converter.state_to_id(database.get_status(company, edition))

def is_state(company, state):
	'''check wether or not the company has the requested state'''
	current_state = database.get_status(company, edition)

	return current_state ==  state

def requested_contract(company):
	'''calls is_state with the parameters to check wether or not
	that company has requested his contract'''
	#return is_state(company, participant_converter.id_to_state(2))
	return is_state(company, 2)