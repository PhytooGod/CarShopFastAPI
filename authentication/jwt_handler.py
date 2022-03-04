import time
import jwt
from schemas import Token
import logging

logging.basicConfig(filename="CarShopLogs.log", format='%(asctime)s %(message)s', filemode='a')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

JWT_SECRET = "b35c601c7935899a6c41fc9b374d55b4be7ce4283d5ed3f8b68af2e4d64a4cc7"
JWT_ALGORITHM = "HS256"

def token_response(token: Token, response_model=Token):
    logging.info("token response function called and token returned")
    return token

def signJWT(username : str):
    logging.debug("singJWT function called")
    payload = {
        "username" : username,
        "expires" : time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm = JWT_ALGORITHM)
    logging.info("username with expire date is encoded")
    return token_response(token)

def decodeJWT(token : str):
    logging.debug("decodeJWT function called")
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithm=JWT_ALGORITHM)
        logging.info("decoded token is being checked if its expire time is valid")
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}