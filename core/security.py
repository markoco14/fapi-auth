from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

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
	return jwt.encode(payload, settings.JWT_SECRET, algorithm=[settings.JWT_ALGORITHM])
