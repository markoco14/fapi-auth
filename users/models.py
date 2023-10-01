from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime, func
from core.database import Base

class UserModel(Base):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True, index=True)
	first_name = Column(String(100))
	last_name = Column(String(100))
	email = Column(String(length=256), unique=True)
	hashed_password = Column(String(length=256))
	is_active = Column(Boolean, default=True)
	is_verified = Column(Boolean, default=False)
	verified_at = Column(DateTime, nullable=True, default=None)
	registered_at = Column(DateTime, nullable=True, default=None)
	created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
	updated_at = Column(DateTime(timezone=True), nullable=True, default=None, onupdate=func.now())