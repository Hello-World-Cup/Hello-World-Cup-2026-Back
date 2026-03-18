from app.domain.dtos.user_dto import UserResponseDTO
from app.domain.exceptions.base_exceptions import UnauthorizedException
from app.ports.driving.handler_interface import HandlerInterface
from app.ports.driven.database.postgres.user_repository_abc import (
    UserRepositoryInterface,
)


class GetCurrentUserHandler(HandlerInterface):
    def __init__(self, user_repository: UserRepositoryInterface) -> None:
        self._user_repository = user_repository

    def execute(self, user_id: int) -> UserResponseDTO:
        user = self._user_repository.get_by_id(user_id)
        if not user:
            raise UnauthorizedException("User does not exist or session is invalid")
        return user
