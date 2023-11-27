import secrets
from typing import List

from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, EmailStr


class Settings(BaseSettings):
    PROJECT_NAME: str = "interview-gpt"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    CLIENT_URL: str = "http://localhost:3000"

    EMAIL_TEST_USER: EmailStr = "test@example.com"  # type: ignore
    FIRST_SUPERUSER: EmailStr = "test123@yahoo.com"
    FIRST_SUPERUSER_PASSWORD: str = "somepassword123$"

    class Config:
        case_sensitive = True


settings = Settings()
