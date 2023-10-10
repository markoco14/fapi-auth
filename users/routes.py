from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import get_db
from auth.utils import oauth2_scheme
from users.models import UserModel
from users.schemas import UserCreate, User
from users.services import create_user_account
from users.utils import get_user_from_token

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

user_router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(oauth2_scheme), Depends(get_user_from_token)]
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def create_user(data: UserCreate, db: Session  = Depends(get_db)):
    create_user_account(data=data, db=db)

    return {"detail": "User account created!"}

@user_router.get("/me", status_code=status.HTTP_200_OK, response_model=User)
def get_current_user(user: User = Depends(get_user_from_token), db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")
    user_response = db.query(UserModel).filter(UserModel.id == user).first()

    return user_response
