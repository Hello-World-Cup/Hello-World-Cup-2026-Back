from pydantic_settings import BaseSettings  # type: ignore

from app.domain.enums import Environment


class Settings(BaseSettings):
    PYTHONUNBUFFERED: int = 1
    LOGGING_LEVEL: str = "DEBUG"
    POSTGRES_URI: str

    ENVIRONMENT: Environment
    CLEAR_EXISTING_DATA_FOR_DEVELOPMENT: bool

    JWT_SECRET: str = "dev-secret-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 15
    JWT_REFRESH_EXPIRE_DAYS: int = 7

    DB_POOL_PRE_PING: bool = True
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_POOL_RECYCLE: int = 300

    API_BASE_URL: str = "http://localhost:8000"

    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_FROM_EMAIL: str | None = None
    SMTP_FROM_NAME: str = "HWC"


settings = Settings()