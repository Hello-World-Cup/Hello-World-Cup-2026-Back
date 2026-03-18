from datetime import datetime, timedelta, timezone
import hashlib
from jose import jwt  # type: ignore

from app.domain.config import settings
from app.domain.dtos.user_dto import RefreshTokenInputDTO, RefreshTokenResponseDTO
from app.domain.exceptions.base_exceptions import UnauthorizedException
from app.ports.driving.handler_interface import HandlerInterface
from app.ports.driven.database.postgres.refresh_token_repository_abc import RefreshTokenRepositoryInterface
from app.ports.driven.database.postgres.user_repository_abc import UserRepositoryInterface


class RefreshAccessTokenHandler(HandlerInterface):
    def __init__(self, refresh_repo: RefreshTokenRepositoryInterface, user_repo: UserRepositoryInterface) -> None:
        self._refresh_repo = refresh_repo
        self._user_repo = user_repo

    def execute(self, data: RefreshTokenInputDTO) -> RefreshTokenResponseDTO:
        now = datetime.now(timezone.utc)
        token_hash = hashlib.sha256(data.refresh_token.encode("utf-8")).hexdigest()

        stored = self._refresh_repo.get_by_hash(token_hash)
        if not stored:
            raise UnauthorizedException("Invalid refresh token")

        if stored.revoked_at is not None:
            raise UnauthorizedException("Refresh token revoked")

        expires_at = stored.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        if expires_at < now:
            raise UnauthorizedException("Refresh token expired")

        # (optional) confirm user still exists
        # user = self._user_repo.get_by_email(...) -> we only have user_id here, so it can be omitted
        user_id = stored.user_id

        # ROTATION: create new refresh token, revoke the old one pointing to the new
        new_refresh_raw = self._new_refresh_raw()
        new_refresh_hash = hashlib.sha256(new_refresh_raw.encode("utf-8")).hexdigest()

        new_row = self._refresh_repo.create(
            user_id=user_id,
            token_hash=new_refresh_hash,
            issued_at=now,
            expires_at=now + timedelta(days=settings.JWT_REFRESH_EXPIRE_DAYS),
        )

        self._refresh_repo.revoke(
            token_id=stored.id,
            revoked_at=now,
            replaced_by_token_id=new_row.id,
        )

        # new access token
        new_access = self._create_access_token(user_id=user_id)

        return RefreshTokenResponseDTO(
            access_token=new_access,
            refresh_token=new_refresh_raw,
            token_type="bearer",
        )

    def _new_refresh_raw(self) -> str:
        import secrets
        return secrets.token_urlsafe(48)

    def _create_access_token(self, user_id: int) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
        payload = {"sub": str(user_id), "exp": expire, "iat": datetime.now(timezone.utc)}
        return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)