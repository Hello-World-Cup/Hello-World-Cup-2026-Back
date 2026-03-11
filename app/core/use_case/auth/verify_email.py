from datetime import datetime, timezone

from app.domain.exceptions.base_exceptions import UnauthorizedException
from app.ports.driving.handler_interface import HandlerInterface
from app.ports.driven.database.postgres.user_repository_abc import (
    UserRepositoryInterface,
)


class VerifyEmailHandler(HandlerInterface):
    def __init__(self, user_repository: UserRepositoryInterface) -> None:
        self._user_repository = user_repository

    def execute(self, token: str) -> dict:
        user = self._user_repository.get_by_verification_token(token)
        if not user or not user.verification_expires_at:
            raise UnauthorizedException("Invalid or expired verification token")

        now = datetime.now(timezone.utc)
        expires_at = user.verification_expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)

        if expires_at < now:
            raise UnauthorizedException("Invalid or expired verification token")

        self._user_repository.confirm_email_verification(user.id)  # type: ignore[arg-type]

        return {"message": "Email verified successfully"}
