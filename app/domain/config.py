from pydantic_settings import BaseSettings # type: ignore

from app.domain.enums import Environment

class Settings(BaseSettings):
    PYTHONUNBUFFERED: int=1
    LOGGING_LEVEL: str="DEBUG"
    POSTGRES_URI: str

    ENVIRONMENT: Environment
    CLEAR_EXISTING_DATA_FOR_DEVELOPMENT: bool

    DB_POOL_PRE_PING: bool=(
        True  # Test connections before use to avoid stale connections
    )
    DB_POOL_SIZE: int=10  # Base connections in pool
    DB_MAX_OVERFLOW: int=20  # Max connections in pool
    DB_POOL_RECYCLE: int=300  # Recycle connections after 300 seconds (5 minutes)


settings=Settings()
