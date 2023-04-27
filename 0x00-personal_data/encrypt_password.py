#!/usr/bin/env python3
""" Encripting passwords
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ Function that expects onet string and return a hashed password
    """
    en_pass = password.encode()
    hashed = bcrypt.hashpw(en_pass, bcrypt.gensalt())

    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ Function that expects 2 arguments and returns a boolean
    """
    valid = False
    en_pass = password.encode()
    if bcrypt.checkpw(en_pass, hashed_password):
        valid = True
    return valid
