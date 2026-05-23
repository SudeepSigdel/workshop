from .config import settings
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from .database import SESSION
from .models import User

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
TOKEN_EXPIRATION_TIME = settings.token_expiration_time

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_token(payload: dict):
    expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRATION_TIME)
    payload.update({"exp": expire})
    token = jwt.encode(payload, SECRET_KEY, ALGORITHM)
    return token

def verify_token(token, credentials_error):
    try:
        payload = jwt.decode(token, SECRET_KEY, [ALGORITHM])
        user_id=payload["user_id"]
        if not user_id:
            raise credentials_error
        return user_id
        
    except JWTError:
        raise credentials_error
    
def get_current_user(db: SESSION, token=Depends(oauth2_scheme)):
    credentials_error = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Couldn't Validate Credentials", headers={"WWW_Authenticate":"Bearer"})
    user_id = verify_token(token, credentials_error)
    user= db.get(User, user_id)
    return user