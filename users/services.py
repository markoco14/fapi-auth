from typing import Annotated
from datetime import datetime

from fastapi import Depends
from fastapi.exceptions import HTTPException

from auth.utils import get_password_hash
from core.database import db_dependency
from users.models import UserModel
from users.schemas import UserCreate

def create_user_account(data: Annotated[UserCreate, Depends()], db: db_dependency):
    user = db.query(UserModel).filter(UserModel.email == data.email).first()
    if user:
        raise HTTPException(status_code=422, detail="Unable to register with that email.")

    new_user = UserModel(
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        hashed_password=get_password_hash(data.password),
        is_active=True,
        is_verified=False,
        registered_at=datetime.now(),
        updated_at=datetime.now()
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
