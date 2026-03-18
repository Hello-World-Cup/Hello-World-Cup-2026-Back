from datetime import datetime
from sqlalchemy.orm import Session

from app.adapters.database.postgres.models.refresh_token_model import RefreshToken
from app.ports.driven.database.postgres.refresh_token_repository_abc import RefreshTokenRepositoryInterface


class RefreshTokenRepository(RefreshTokenRepositoryInterface):
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, user_id: int, token_hash: str, issued_at: datetime, expires_at: datetime,
               user_agent: str | None = None, ip_address: str | None = None):
        rt = RefreshToken(
            user_id=user_id,
            token_hash=token_hash,
            issued_at=issued_at,
            expires_at=expires_at,
            user_agent=user_agent,
            ip_address=ip_address,
        )
        self.db.add(rt)
        self.db.commit()
        self.db.refresh(rt)
        return rt

    def get_by_hash(self, token_hash: str):
        return self.db.query(RefreshToken).filter(RefreshToken.token_hash == token_hash).first()

    def revoke(self, token_id: int, revoked_at: datetime, replaced_by_token_id: int | None = None) -> None:
        rt = self.db.query(RefreshToken).filter(RefreshToken.id == token_id).first()
        if not rt:
            return
        rt.revoked_at = revoked_at
        rt.replaced_by_token_id = replaced_by_token_id
        self.db.add(rt)
        self.db.commit()

    def revoke_all_for_user(self, user_id: int, revoked_at: datetime) -> None:
        self.db.query(RefreshToken).filter(
            RefreshToken.user_id == user_id,
            RefreshToken.revoked_at.is_(None),
        ).update({"revoked_at": revoked_at})
        self.db.commit()