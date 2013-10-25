import bcrypt

def encrypt(password):
	'''Encrypts the password
	Everything tastes better with salt'''
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt(12))
    return hashed_password

def is_equal(hashed, password):
	'''Does given password correspondend to given salted password'''
    try:
        return (bcrypt.hashpw(password, hashed) == hashed)
    except:
        return False
