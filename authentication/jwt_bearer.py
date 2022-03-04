from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .jwt_handler import decodeJWT
import logging

logging.basicConfig(filename="CarShopLogs.log", format='%(asctime)s %(message)s', filemode='a')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class jwtBearer(HTTPBearer):
    def __init__(self, auto_error : bool = True):
        super(jwtBearer, self).__init__(auto_error=auto_error)
    
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(jwtBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                logging.error(f"Wrong authentication scheme|status code=403")
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                logging.error(f"Invalid or expired token|status code=403")
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")  
            logging.info("valid token is returned")
            return credentials.credentials
        else:
            logging.error(f"Invalid authorization code|status code=403")
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid