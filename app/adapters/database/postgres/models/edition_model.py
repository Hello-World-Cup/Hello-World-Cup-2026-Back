from sqlalchemy import Column, Integer, String, DateTime

from app.adapters.database.postgres.connection import Base


class Edition(Base):
    __tablename__="edition"

    id=Column(Integer, primary_key=True)
    name=Column (String, nullable=False)
    start_date=Column (DateTime, nullable=False)
    end_date=Column (DateTime, nullable=False)
