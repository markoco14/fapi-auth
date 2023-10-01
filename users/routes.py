from fastapi import APIRouter, Request, status, Depends
from sqlalchemy.orm import Session
from users.models import UserModel
from users.responses import UserResponse
from users.schemas import CreateUserRequest

from core.database import get_db
from users.services import create_user_account
from core.security import oauth2_scheme, get_current_user

router = APIRouter(
	prefix="/users",
	tags=["users"]
)

user_router = APIRouter(
	prefix="/users",
	tags=["users"],
	dependencies=[Depends(oauth2_scheme), Depends(get_current_user)]
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def create_user(data: CreateUserRequest, db: Session  = Depends(get_db)):
	create_user_account(data=data, db=db)

	return {"detail": "User account created!"}

@user_router.get("/me", status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_current_user(request: Request):
	return request.user