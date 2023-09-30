from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from auth.services import get_token

from core.database import get_db

router = APIRouter(
	prefix="/auth",
	tags=["auth"]
)

@router.post("/token", status_code=status.HTTP_200_OK)
def authenticate_user(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
	return get_token(data=data, db=db)
