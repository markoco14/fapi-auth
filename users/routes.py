from fastapi import APIRouter, Request, status, Depends
from sqlalchemy.orm import Session
from users.models import UserModel
from users.schemas import CreateUserRequest

from core.database import get_db
from users.services import create_user_account

router = APIRouter(
	prefix="/users",
	tags=["users"]
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def create_user(data: CreateUserRequest, db: Session  = Depends(get_db)):
	create_user_account(data=data, db=db)

	return {"detail": "User account created!"}

@router.get("/me", status_code=status.HTTP_200_OK)
def get_current_user(request: Request):
	return request.user