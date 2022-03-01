import time
import jwt
from schemas import Token

JWT_SECRET = "b35c601c7935899a6c41fc9b374d55b4be7ce4283d5ed3f8b68af2e4d64a4cc7"
JWT_ALGORITHM = "HS256"

def token_response(token: Token, response_model=Token):
    return token

def signJWT(username : str):
    payload = {
        "username" : username,
        "expires" : time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm = JWT_ALGORITHM)
    return token_response(token)

def decodeJWT(token : str):
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}