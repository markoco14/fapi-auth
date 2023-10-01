from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from auth.responses import TokenResponse
from core.config import get_settings
from core.database import db_dependency
from core.security import get_token_payload, verify_password, create_access_token, create_refresh_token
from users.models import UserModel
from datetime import timedelta, datetime

settings = get_settings()

def get_token(data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
	user = db.query(UserModel).filter(UserModel.email == data.username).first()

	if not user:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST, 
			detail="User not found",
			headers={"WWW-Authenticate": "Bearer"}
			)
	
	if not verify_password(plain_password=data.password, hashed_password=user.hashed_password):
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="Invalid login credentials",
			headers={"WWW-Authenticate": "Bearer"}
		)
	
	check_user_active(user=user)

	check_user_verified(user=user)

	return _get_user_token(user=user)
	
	
def check_user_active(user: UserModel):
	if not user.is_active:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST, 
			detail="Your account is inactive. Please contact support.",
			headers={"WWW-Authenticate": "Bearer"}
			)
	
"""
let user be unverified for 30 days
"""
def check_user_verified(user: UserModel):
	within_thirty_days = datetime.now() - timedelta(days=30)
	if not user.is_verified and user.created_at >= within_thirty_days:
		return True
	
	if not user.is_verified:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST, 
			detail="Your account is not verified. We have resent the account verification email.",
			headers={"WWW-Authenticate": "Bearer"}
			)
	

	
	
def _get_user_token(user: UserModel, refresh_token: str = None):
	payload = {"id": user.id }

	access_token_expiry = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

	access_token = create_access_token(data=payload, expiry=access_token_expiry)
	if not refresh_token:
		refresh_token = create_refresh_token(data=payload)

	return TokenResponse(
		access_token=access_token,
		refresh_token=refresh_token,
		expires_in=access_token_expiry.seconds
	)


def get_refresh_token(token: str, db: db_dependency):
	payload = get_token_payload(token=token)
	user_id = payload.get("id", None)
	if not user_id:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Invalid refresh token",
			headers={"WWW-Authenticate": "Bearer"}
		)
	
	user = db.query(UserModel).filter(UserModel.id == user_id).first()
	if not user:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Invalid refresh token",
			headers={"WWW-Authenticate": "Bearer"}
		)
	return _get_user_token(user=user, refresh_token=token)


	
	