from sqlalchemy import Column, Integer, String, ForeignKey

from app.adapters.database.postgres.connection import Base


class Team(Base):
    __tablename__="team"

    id=Column(Integer, primary_key=True)
    name=Column(String, nullable=False)
    logo=Column(String)
    score=Column(Integer)
    standing_position=Column(Integer)
    cloud_repo_link=Column(String)
    
    edition_id = Column(
        Integer, ForeignKey("edition.id", ondelete="CASCADE"), nullable=False
    )
    category_id = Column(
        Integer, ForeignKey("category.id", ondelete="CASCADE"), nullable=False
    )
    evaluation_id = Column(
        Integer, ForeignKey("evaluation.id", ondelete="SET NULL"), nullable=True
    )
    assigned_evaluator_id = Column(
        Integer, ForeignKey("user.id", ondelete="SET NULL"), nullable=True
    )
