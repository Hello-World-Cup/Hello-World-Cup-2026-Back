from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.adapters.database.postgres.connection import Base


class RefreshToken(Base):
    __tablename__ = "refresh_token"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True)

    token_hash = Column(String, nullable=False, unique=True, index=True)

    issued_at = Column(DateTime(timezone=True), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)

    revoked_at = Column(DateTime(timezone=True), nullable=True)

    replaced_by_token_id = Column(Integer, nullable=True)  # for token rotation

    user_agent = Column(String, nullable=True)
    ip_address = Column(String, nullable=True)