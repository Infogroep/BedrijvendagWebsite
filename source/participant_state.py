import database, participant_converter
from config import edition, participant_states

def get_state_ID(company):
	return state_to_id(database.get_status(company, edition))

def is_state(company, state):
	current_state = database.get_status(company, edition)

	return current_state ==  state

def requested_contract(company):
	return is_state(company, id_to_state(2))
