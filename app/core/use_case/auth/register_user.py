import secrets
from datetime import datetime, timedelta, timezone

from passlib.context import CryptContext  # type: ignore

from app.domain.config import settings
from app.domain.dtos.user_dto import CreateUserDTO, RegisterUserInputDTO, UserResponseDTO
from app.domain.enums import UserStatus
from app.domain.exceptions.base_exceptions import (
    InvalidCredentialsException,
    RecordNotFoundException,
)
from app.ports.driven.database.postgres.role_repository import RoleRepositoryInterface
from app.ports.driving.handler_interface import HandlerInterface
from app.ports.driven.database.postgres.user_repository_abc import UserRepositoryInterface
from app.ports.driven.email.email_sender_interface import EmailSenderInterface

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


class RegisterUserHandler(HandlerInterface):
    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        role_repository: RoleRepositoryInterface,
        email_sender: EmailSenderInterface,
    ) -> None:
        self._user_repository = user_repository
        self._role_repository = role_repository
        self._email_sender = email_sender

    def execute(self, data: RegisterUserInputDTO) -> UserResponseDTO:
        password_hash = pwd_context.hash(data.password)
        normalized_email = data.email.strip().lower()

        token = secrets.token_urlsafe(32)
        expires_at = datetime.now(timezone.utc) + timedelta(hours=24)

        default_role = self._role_repository.get_by_internal_code("common_user")

        if not default_role:
            raise RecordNotFoundException("role")

        user = self._user_repository.create_or_replace_pending(
            CreateUserDTO(
                name=data.name,
                email=normalized_email,
                password_hash=password_hash,
                portrait=data.portrait,
                status=UserStatus.PENDING,
                verification_token=token,
                verification_expires_at=expires_at,
                is_verified=False,
                role_id=default_role.id,
            )
        )

        verify_link = f"{settings.API_BASE_URL}/auth/verify?token={token}"

        if not user.email or not user.name:
            raise InvalidCredentialsException()

        self._email_sender.send_verification_email(
            to_email=user.email,
            user_name=user.name,
            verify_link=verify_link,
        )

        return user
