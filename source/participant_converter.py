from config import participant_states

def id_to_state(id):
	'''Given an id, it will return the corresponding state as string. id will be converted to a integer intput may be a string containting the id'''
	state = False
	for state_tuple in participant_states:
		print state_tuple
		if state_tuple[0] == int(id):
			state = state_tuple[1]
			break
	return state

def state_to_id(state):
	'''Given an state as string, This function will return the id as int'''
	ID = False
	for state_tuple in participant_states:
		if state_tuple[1] == state:
			ID = state_tuple[0]
			break
	return ID
