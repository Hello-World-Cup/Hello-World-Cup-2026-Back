from sqlalchemy import Column, Integer, String, ForeignKey

from app.adapters.database.postgres.connection import Base


class Evaluation(Base):
    __tablename__="evaluation"

    id=Column(Integer, primary_key=True)
    file_name=Column(String, nullable=False)

    category_id = Column(
        Integer, ForeignKey("category.id", ondelete="CASCADE"), nullable=False
    )
