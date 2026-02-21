from passlib.context import CryptContext  # type: ignore

from app.domain.dtos.user_dto import RegisterUserInputDTO, UserResponseDTO
from app.ports.driving.handler_interface import HandlerInterface
from app.ports.driven.database.postgres.user_repository_abc import UserRepositoryInterface

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


class RegisterUserHandler(HandlerInterface):
    def __init__(self, user_repository: UserRepositoryInterface) -> None:
        self._user_repository = user_repository

    def execute(self, data: RegisterUserInputDTO) -> UserResponseDTO:
        password_hash = pwd_context.hash(data.password)
        return self._user_repository.create(
            name=data.name,
            email=data.email,
            password_hash=password_hash,
            portrait=data.portrait,
            status=data.status,
        )
