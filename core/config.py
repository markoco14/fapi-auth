import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings	

env_path = Path(".") / ".env"

load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):

	# Database
	DB_USER: str = os.environ.get('DB_USER')
	DB_PASSWORD: str = os.environ.get('DB_PASSWORD')
	DB_HOST: str = os.environ.get('DB_HOST')
	DB_PORT: str = os.environ.get('DB_PORT')
	DB_NAME: str = os.environ.get('DB_NAME')
	DATABASE_URL: str = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

	# JWT
	JWT_SECRET: str = os.environ.get('JWT_SECRET')
	JWT_ALGORITHM: str = os.environ.get('JWT_ALGORITHM')
	ACCESS_TOKEN_EXPIRE_MINUTES: int = os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES')

"""
	can I declare this within the class?
	but I would have to create a new instance wherever I want to use it?
	this way I can do import config -> var = config.get_settings()

	as method on class I would have to say var = Settings()
	var.get_settings()

	TODO: talk to Kos
"""
# or from config import get_settings -> var = get_settings()
def get_settings() -> Settings:
	return Settings()
