from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select
from ..database import SESSION
from .. import models, utils, oauth2

router= APIRouter(
    tags=["Login"],
    prefix="/login"
)

@router.post("/")
def login(db: SESSION, user_credentials: OAuth2PasswordRequestForm = Depends()):
    user = db.exec(select(models.User).where(user_credentials.username == models.User.email)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    access_token = oauth2.create_token({"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}