from datetime import datetime, timedelta
from typing import Annotated
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from fastapi import Depends, Request
from core.database import get_db
from users.models import UserModel
from sqlalchemy.orm import Session

from starlette.authentication import AuthCredentials, UnauthenticatedUser

from core.config import get_settings

settings = get_settings()

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_password_hash(password: str):
	return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
	return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data, expiry: timedelta):
	payload = data.copy()
	expire_in = datetime.utcnow() + expiry
	payload.update({"exp": expire_in})
	return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

"""
creates a refresh token with default 3 day expiry
"""
def create_refresh_token(data, expiry: timedelta = timedelta(days=3)):
	# Can add JWT_REFRESH_SECRET
	payload = data.copy()
	expire_in = datetime.utcnow() + expiry
	payload.update({"exp": expire_in})
	return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def get_token_payload(token: str):
	try:
		payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
	except JWTError:
		return None
	return payload

def get_current_user(access_token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[Session, Depends(get_db)] = None):
	payload = get_token_payload(token=access_token)
	if not payload or type(payload) is not dict:
		return None
	
	user_id = payload.get("id", None)
	if not user_id:
		return None
	
	if not db:
		db = next(get_db())

	user = db.query(UserModel).filter(UserModel.id == user_id).first()

	return user


class JWTAuth:

	async def authenticate(self, request: Request):
		guest = AuthCredentials(['unauthenicated']), UnauthenticatedUser()
		
		if 'authorization' not in request.headers:
			return guest
		
		access_token = request.headers.get("authorization").split(" ")[1] # Bearer token_hash
		if not access_token:
			return guest
		
		user = get_current_user(access_token=access_token)

		if not user:
			return guest
		
		return AuthCredentials('authenticated'), user