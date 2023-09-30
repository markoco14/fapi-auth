from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from users.schemas import CreateUserRequest

from core.database import get_db

router = APIRouter(
	prefix="/users",
	tags=["users"]
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def create_user(data: CreateUserRequest, db: Session  = Depends(get_db)):
	pass