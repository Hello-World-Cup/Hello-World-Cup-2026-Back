from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.declarative import DeclarativeMeta
from app.domain.config import settings

DATABASE_URI = settings.POSTGRES_URI
engine = create_engine(
    DATABASE_URI,
    pool_pre_ping=settings.DB_POOL_PRE_PING,
    pool_recycle=settings.DB_POOL_RECYCLE,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_reset_on_return="rollback",
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
)
Base: DeclarativeMeta = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
