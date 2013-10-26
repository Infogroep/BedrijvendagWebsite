import database, participant_converter
from config import edition, participant_states

def get_state_ID(company, edition):
	'''Get the id of the state where the company is currently in'''
	return participant_converter.state_to_id(database.get_status(company, edition))

def is_state(company, states):
	'''check wether or not the company has the requested state'''
	current_state = get_state_ID(company, edition)

	res = False
	for state in states:
		if current_state == state:
			res = True
			break

	return res

def requested_contract(company):
	'''calls is_state with the parameters to check wether or not
	that company has requested his contract'''
	#return is_state(company, participant_converter.id_to_state(2))
	return is_state(company, (3, 4, 5))