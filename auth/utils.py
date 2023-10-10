from datetime import timedelta, datetime
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from core.database import settings
from passlib.context import CryptContext

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

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
		return payload
	except JWTError:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token.")

