import os
import secrets
from datetime import datetime, timedelta, timezone

from passlib.context import CryptContext  # type: ignore

from app.domain.dtos.user_dto import RegisterUserInputDTO, UserResponseDTO
from app.ports.driving.handler_interface import HandlerInterface
from app.ports.driven.database.postgres.user_repository_abc import UserRepositoryInterface
from app.adapters.email.gmail_smtp_sender import GmailSmtpSender  # lo creas en el paso 3

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


class RegisterUserHandler(HandlerInterface):
    def __init__(self, user_repository: UserRepositoryInterface) -> None:
        self._user_repository = user_repository

    def execute(self, data: RegisterUserInputDTO) -> UserResponseDTO:
        password_hash = pwd_context.hash(data.password)

        # 1) token + expiración
        token = secrets.token_urlsafe(32)
        expires_at = datetime.now(timezone.utc) + timedelta(hours=24)

        # 2) crear usuario guardando token/expiry y verified=false
        user = self._user_repository.create(
            name=data.name,
            email=data.email,
            password_hash=password_hash,
            portrait=data.portrait,
            status=data.status,
            verification_token=token,
            verification_expires_at=expires_at,
            is_verified=False,
        )

        # 3) enviar email con link
        api_base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
        verify_link = f"{api_base_url}/auth/verify?token={token}"

        GmailSmtpSender().send_verification_email(
            to_email=user.email,
            user_name=user.name,
            verify_link=verify_link,
        )

        return user