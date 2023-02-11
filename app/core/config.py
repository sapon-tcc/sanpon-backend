import os

from pydantic import AnyHttpUrl, BaseSettings, HttpUrl, EmailStr
from typing import List

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SERVER_HOST: AnyHttpUrl = "http://localhost"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    PROJECT_NAME: str = "sapon-backend"
    FIRST_SUPERUSER: EmailStr = "admin@admin.com"
    FIRST_SUPERUSER_PASSWORD: str = "admin"
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    # Set to enviroment
    SECRET_KEY = os.environ.get("SECRET_KEY")
    MONGODB_URL: str = os.environ.get("MONGODB_URL")

    class Config:
        case_sensitive = True


settings = Settings()

