from pydantic_settings import BaseSettings 

from app.domain.enums import Environment

class Settings(BaseSettings):
    PYTHONUNBUFFERED: int=1
    LOGGING_LEVEL: str="DEBUG"
    POSTGRES_URI: str
    SUPABASE_URL: str
    SUPABASE_SERVICE_ROLE_KEY: str

    ENVIRONMENT: Environment
    CLEAR_EXISTING_DATA_FOR_DEVELOPMENT: bool

    DB_POOL_PRE_PING: bool=(
        True  
    )
    DB_POOL_SIZE: int=10  
    DB_MAX_OVERFLOW: int=20  
    DB_POOL_RECYCLE: int=300 


settings=Settings()
