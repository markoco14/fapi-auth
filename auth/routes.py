from typing import Annotated
from fastapi import APIRouter, status, Depends, Header
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from auth.services import get_token, refresh_user_token

from core.database import get_db

router = APIRouter(
	prefix="/auth",
	tags=["auth"]
)

@router.post("/token", status_code=status.HTTP_200_OK)
def login(data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(get_db)]):
	return get_token(data=data, db=db)

@router.post("/refresh", status_code=status.HTTP_200_OK)
def refresh_access_token(refresh_token: Annotated[str, Header()], db: Annotated[Session, Depends(get_db)]):
	return refresh_user_token(refresh_token=refresh_token, db=db)