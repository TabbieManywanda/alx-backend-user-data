#!/usr/bin/env python3

'''Implementing a hash_password function'''

import bcrypt


def hash_password(password: str) -> bytes:
    '''returns a salted, hashed password,
    which is a byte string'''

    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    '''checks if password is valid and
    returns a boolean'''

    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
