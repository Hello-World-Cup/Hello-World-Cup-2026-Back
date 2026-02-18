from sqlalchemy import Column, Integer, String, DateTime

from app.adapters.database.postgres.connection import Base


class Category(Base):
    __tablename__="category"

    id=Column(Integer, primary_key=True)
    name=Column(String, nullable=False)
    open_date=Column(DateTime, nullable=False)
    close_date=Column(DateTime, nullable=False)
    internal_code=Column(String, nullable=False)
