from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Table

from app.adapters.database.postgres.connection import Base
from app.domain.enums import UserStatus, TeamRequestStatus


class User(Base):
    __tablename__="user"

    id=Column(Integer, primary_key=True)
    username=Column(String, nullable=False, index=True)
    name=Column(String, nullable=False)
    email=Column(String, nullable=False)
    password_hash=Column(String, nullable=False)
    portrait=Column(String)
    status=Column(Enum(UserStatus), nullable=False)

    role_id = Column(Integer, ForeignKey("role.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(
        Integer, ForeignKey("category.id", ondelete="CASCADE")
    )

user_team_association=Table(
    "user_team_association",
    Base.metadata,  # type: ignore
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("team_id", Integer, ForeignKey("team.id"), primary_key=True),
)

team_request_association=Table(
    "team_request_association",
    Base.metadata,  # type: ignore
    Column("id", Integer, primary_key=True),
    Column("team_id", Integer, ForeignKey("team.id")),
    Column("sender_user_id", Integer, ForeignKey("user.id")),
    Column("receiver_user_id", Integer, ForeignKey("user.id")),
    Column("status", Enum(TeamRequestStatus)),
)
