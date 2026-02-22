from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext  # type: ignore
from jose import jwt  # type: ignore

from app.domain.dtos.user_dto import LoginInputDTO, LoginResponseDTO, UserResponseDTO
from app.ports.driving.handler_interface import HandlerInterface
from app.ports.driven.database.postgres.user_repository_abc import UserRepositoryInterface
from app.domain.exceptions.base_exceptions import InvalidCredentialsException
from app.domain.config import settings

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


class LoginUserHandler(HandlerInterface):
    def __init__(self, user_repository: UserRepositoryInterface) -> None:
        self._user_repository = user_repository

    def execute(self, data: LoginInputDTO) -> LoginResponseDTO:
        user = self._user_repository.get_by_email(data.email)

        if user is None:
            raise InvalidCredentialsException()

        if not pwd_context.verify(data.password, user.password_hash):
            raise InvalidCredentialsException()

        if data.name.strip().lower() != getattr(user, "name", "").strip().lower():
            raise InvalidCredentialsException()

        access_token = self._create_access_token(user.id, user.email)
        user_response = UserResponseDTO.from_orm(user)

        return LoginResponseDTO(
            access_token=access_token,
            token_type="bearer",
            user=user_response,
        )

    def _create_access_token(self, user_id: int, email: str) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
        payload = {
            "sub": str(user_id),
            "email": email,
            "exp": expire,
            "iat": datetime.now(timezone.utc),
        }
        return jwt.encode(
            payload,
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM,
        )
