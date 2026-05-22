from fastapi import APIRouter
from .. import models, utils
from ..database import SESSION

router= APIRouter(
    tags=["User Signup"],
    prefix="/users"
)

@router.post("/", status_code=201, response_model=models.UserResponse)
def user_signup(user_info: models.UserCreate, db: SESSION):
    user_info.password = utils.hash_password(user_info.password)
    user = models.User.model_validate(user_info)
    db.add(user)
    db.commit()
    db.refresh(user)

    return user