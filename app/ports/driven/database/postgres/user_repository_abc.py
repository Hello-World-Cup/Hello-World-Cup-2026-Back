from abc import ABC, abstractmethod
from app.domain.dtos.user_dto import UserResponseDTO
from app.domain.enums import UserStatus


class UserRepositoryInterface(ABC):
    @abstractmethod
    def create(
        self,
        name: str,
        email: str,
        password_hash: str,
        portrait: str | None = None,
        status: UserStatus | None = None,
    ) -> UserResponseDTO:
        raise NotImplementedError("Create method not implemented!")
