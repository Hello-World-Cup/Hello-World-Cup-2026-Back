from abc import ABC, abstractmethod

from app.domain.dtos.user_dto import CreateUserDTO, UserDTO, UserResponseDTO


class UserRepositoryInterface(ABC):
    @abstractmethod
    def get_by_email(self, email: str) -> UserDTO | None:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, user_id: int) -> UserResponseDTO | None:
        raise NotImplementedError

    @abstractmethod
    def get_by_verification_token(self, token: str) -> UserDTO | None:
        raise NotImplementedError

    @abstractmethod
    def create(self, data: CreateUserDTO) -> UserResponseDTO:
        raise NotImplementedError

    @abstractmethod
    def create_or_replace_pending(self, data: CreateUserDTO) -> UserResponseDTO:
        raise NotImplementedError

    @abstractmethod
    def confirm_email_verification(self, user_id: int) -> None:
        raise NotImplementedError
