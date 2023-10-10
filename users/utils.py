from typing import Annotated
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from core.config import get_settings
from auth.utils import oauth2_scheme


settings = get_settings()


def get_user_from_token(access_token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token=access_token, key=settings.JWT_SECRET, algorithms=[
                             settings.JWT_ALGORITHM])
        user_id: int = payload.get("id", None)
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Could not validate user")
        return user_id

    except JWTError:
        return None
