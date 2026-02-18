from sqlalchemy import Column, Integer, String, Boolean

from app.adapters.database.postgres.connection import Base


class Role(Base):
    __tablename__="role"

    id=Column(Integer, primary_key=True)
    name=Column(String, nullable=False)
    description=Column(String, nullable=False)
    is_super_user=Column(Boolean, nullable=False, default=False)
    internal_code=Column(String, nullable=False)
