from sqlalchemy import Column, String, Text, Integer, Boolean
from database import Base

class User(Base):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True, index=True)
	email = Column(String(length=None), unique=True)
	hashed_password = Column(String(length=None))