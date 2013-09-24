import hashlib, uuid

def encrypt(password):
    hashed_password = hashlib.sha512(password).hexdigest()
    return hashed_password
