import time
import datetime
import jwt
# from src.config.config import JWT_PRIVATE_KEY

with open("private.pem", "r") as f:
    JWT_PRIVATE_KEY = f.read()
    
with open("public.pem", "r") as f:
    JWT_PUBLIC_KEY = f.read()

def create_jwt(username):
    curr_time = int(time.time())
    payload = {
        "iss": "Hallway_software",
        "sub": username,
        "aud": "all",
        "role": "user",
        "nbf": curr_time,
        "exp": curr_time + int(datetime.timedelta(hours=1).total_seconds()),
        "iat": curr_time
    }
    token = jwt.encode(payload, JWT_PRIVATE_KEY, algorithm="RS256")
    return token