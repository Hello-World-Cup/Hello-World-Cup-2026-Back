from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext  # type: ignore
from jose import jwt  # type: ignore

import secrets
import hashlib

from app.domain.dtos.user_dto import LoginInputDTO, LoginResponseDTO, UserResponseDTO
from app.ports.driving.handler_interface import HandlerInterface
from app.ports.driven.database.postgres.user_repository_abc import UserRepositoryInterface
from app.ports.driven.database.postgres.refresh_token_repository_abc import RefreshTokenRepositoryInterface
from app.domain.exceptions.base_exceptions import InvalidCredentialsException
from app.domain.config import settings

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


class LoginUserHandler(HandlerInterface):
    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        refresh_repo: RefreshTokenRepositoryInterface,
    ) -> None:
        self._user_repository = user_repository
        self._refresh_repo = refresh_repo

    def execute(self, data: LoginInputDTO) -> LoginResponseDTO:
        normalized_email = data.email.strip().lower()
        user = self._user_repository.get_by_email(normalized_email)

        if user is None:
            raise InvalidCredentialsException(
                message="Invalid credentials",
                field="EMAIL",
            )

        if not pwd_context.verify(data.password, user.password_hash):
            raise InvalidCredentialsException(
                message="Invalid credentials",
                field="PASSWORD",
            )

        if data.name.strip().lower() != getattr(user, "name", "").strip().lower():
            raise InvalidCredentialsException(
                message="Invalid credentials",
                field="NAME",
            )

        if not getattr(user, "is_verified", False):
            raise InvalidCredentialsException(
                message="Email not verified",
                field="EMAIL_NOT_VERIFIED",
            )

        access_token = self._create_access_token(user.id, user.email)
        refresh_token = self._create_refresh_token(user.id)

        user_response = UserResponseDTO.from_orm(user)

        return LoginResponseDTO(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            user=user_response,
        )

    def _create_access_token(self, user_id: int, email: str) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
        payload = {
            "sub": str(user_id),
            "email": email,
            "type": "access",
            "exp": expire,
            "iat": datetime.now(timezone.utc),
        }
        return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

    def _hash_refresh_token(self, token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    def _create_refresh_token(self, user_id: int) -> str:
        now = datetime.now(timezone.utc)
        expires = now + timedelta(days=settings.JWT_REFRESH_EXPIRE_DAYS)

        raw = secrets.token_urlsafe(48)  # opaque token
        token_hash = self._hash_refresh_token(raw)

        self._refresh_repo.create(
            user_id=user_id,
            token_hash=token_hash,
            issued_at=now,
            expires_at=expires,
        )
        return raw