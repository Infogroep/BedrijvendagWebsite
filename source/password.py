import string
import random

import bcrypt


def encrypt(password):
    """Encrypts the password
    Everything tastes better with salt"""
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt(12))
    return hashed_password


def is_equal(hashed, password):
    """Does given password correspond to given salted password"""

    return bcrypt.hashpw(password, hashed) == hashed


def generate_recovery_hash(size=30, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for x in range(size))