import config


def upload(field, enrollment_number, raw):
    """Takes the field of study of the student,
    it's enrollment number to check and the raw
    pdf file the file gets saved in the directory
    of the corresponding file"""

    filename = config.ROOT + "/" + config.field_directory + "/" + config.edition + "/" + field + "/" + str(
        enrollment_number) + ".pdf"
    resume = open(filename, "w")

    resume.write(raw)

    resume.close()
