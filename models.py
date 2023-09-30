from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime, func
from core.database import Base

class User(Base):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True, index=True)
	email = Column(String(length=256), unique=True)
	hashed_password = Column(String(length=256))
	is_active = Column(Boolean, default=True)
	is_verified = Column(Boolean, default=False)
	created_at = Column(DateTime(timezone=True), server_default=func.now())
	updated_at = Column(DateTime(timezone=True), onupdate=func.now())