from typing import Annotated

from fastapi import Depends
from core.database import db_dependency
from core.security import get_password_hash
from users.models import UserModel
from fastapi.exceptions import HTTPException
from datetime import datetime

from users.schemas import CreateUserRequest

def create_user_account(data: Annotated[CreateUserRequest, Depends()], db: db_dependency):
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