from sqlalchemy import Column, Integer, String, ForeignKey  # noqa: F401

from app.adapters.database.postgres.connection import Base

class Test(Base):
    __tablename__="tests"

    id=Column(Integer, primary_key=True, index=True)
    message=Column(String, nullable=False)
