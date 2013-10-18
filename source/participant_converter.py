from config import participant_states

def id_to_state(id):
	state = False
	for state_tuple in participant_states:
		if state_tuple[0] == id:
			state = state_tuple[1]
			break
	return state

def state_to_id(state):
	ID = False
	for state_tuple in participant_states:
		if state_tuple[1] == id:
			ID = state_tuple[0]
			break
	return ID