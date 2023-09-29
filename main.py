from fastapi import Depends, FastAPI, HTTPException, status
from typing import Annotated, Union, List
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
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


@app.get("/")
def read_root():
    return {"Hello": "World"}