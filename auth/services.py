from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from core.database import SessionLocal, get_db
from core.security import verify_password
from users.models import UserModel


async def get_token(data: OAuth2PasswordRequestForm = Depends(), db: SessionLocal = Depends(get_db)):
	user = db.query(UserModel).filter(UserModel.email == data.username).first()

	if not user:
		raise HTTPException(
			status=status.HTTP_400_BAD_REQUEST, 
			detail="User not found",
			headers={"WWW-Authenticate": "Bearer"}
			)
	
	if not verify_password(plain_password=data.password, hashed_password=user.password):
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="Invalid login credentials",
			headers={"WWW-Authenticate": "Bearer"}
		)
	
	_verify_user_access(user=user)

	return '' # Return access token and refresh token
	

def _verify_user_access(user: UserModel):
	if not user.is_active:
		raise HTTPException(
			status=status.HTTP_400_BAD_REQUEST, 
			detail="Your account is inactive. Please contact support.",
			headers={"WWW-Authenticate": "Bearer"}
			)
	
	# I want to let unverified accounts have some access
	# if not user.is_verified:
	# 	Trigger user account verification email
	# 	raise HTTPException(
	# 		status=status.HTTP_400_BAD_REQUEST, 
	# 		detail="Your account is not verified. We have resent the account verification email.",
	# 		headers={"WWW-Authenticate": "Bearer"}
	# 		)
	