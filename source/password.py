import bcrypt

def encrypt(password):
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt(12))
    return hashed_password

def is_equal(hashed, password):
    try:
        return (bcrypt.hashpw(password, hashed) == hashed)
    except:
        return False
