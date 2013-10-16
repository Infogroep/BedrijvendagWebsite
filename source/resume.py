import config

def upload(field, enrollment_number, raw):

	filename = config.ROOT + "/" + config.field_directory + "/" + field + "/" + str(enrollment_number) + ".pdf"
	resume = open(filename, "w")

	resume.write(raw)

	resume.close()
