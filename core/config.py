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

    ENVIRONMENT: str = os.environ.get('ENVIRONMENT')
    NEXT_DEMO_URL: str = os.environ.get('NEXT_DEMO_URL')

    if ENVIRONMENT == 'dev':
        DATABASE_URL: str = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    else:
        MYSQL_ATTR_SSL_CA: str = os.environ.get('MYSQL_ATTR_SSL_CA')
        DATABASE_URL: str = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?ssl_ca={MYSQL_ATTR_SSL_CA}"

    # JWT
    JWT_SECRET: str = os.environ.get('JWT_SECRET')
    JWT_ALGORITHM: str = os.environ.get('JWT_ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES')


# or from config import get_settings -> var = get_settings()
def get_settings() -> Settings:
    return Settings()
