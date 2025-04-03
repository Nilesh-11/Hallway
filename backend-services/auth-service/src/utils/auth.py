import hashlib
import random

def hash_password(password: str):
    hash_object = hashlib.sha256(password.encode())  
    hash_hex = hash_object.hexdigest()
    return hash_hex

def generate_otp():
    return str(random.randint(100000, 999999))