from fastapi import Depends, FastAPI, HTTPException, status
from typing import Annotated, Union, List
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
import users.models as models

from auth.routes import router as auth_router

from users.routes import router as user_router
from core.database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import auth

app = FastAPI()
# app.include_router(auth.router)
app.include_router(user_router)
app.include_router(auth_router)

# Dependency

# CORS POLICY
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1"
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]
# user_dependency = Annotated[dict, Depends(auth.get_current_user)]

class User(BaseModel):
	email: str

# @app.get("/", status_code=status.HTTP_200_OK)
# def user(user: user_dependency, db: db_dependency):
#     if User is None:
#          raise HTTPException(status_code=401, detail="Authentication failed")
    
#     return {"user": user}