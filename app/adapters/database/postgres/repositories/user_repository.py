from sqlalchemy.orm import Session

from app.adapters.database.postgres.models.user_model import User
from app.ports.driven.database.postgres.user_repository_abc import UserRepositoryInterface
from app.domain.dtos.user_dto import CreateUserDTO, UserDTO, UserResponseDTO
from app.domain.enums import UserStatus
from app.domain.exceptions.base_exceptions import DuplicateRecordException


class UserRepository(UserRepositoryInterface):
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_email(self, email: str) -> UserDTO | None:
        normalized_email = email.strip().lower()
        user = self.db.query(User).filter(User.email == normalized_email).first()
        return UserDTO.from_orm(user) if user else None

    def create(self, data: CreateUserDTO) -> UserResponseDTO:
        # Email is expected to be already normalized by the caller (e.g. RegisterUserHandler)
        email = data.email
        username = email.split("@")[0]

        if self.db.query(User).filter(User.email == email).first():
            raise DuplicateRecordException(
                f"A user with this email already exists: '{email}'", field="EMAIL"
            )

        if self.db.query(User).filter(User.username == username).first():
            raise DuplicateRecordException(
                f"A user with this username already exists: '{username}'", field="USERNAME"
            )

        user_status = data.status if data.status is not None else UserStatus.PENDING
        DEFAULT_ROLE_ID = 2

        user_orm = User(
            username=username,
            name=data.name,
            email=email,
            password_hash=data.password_hash,
            role_id=DEFAULT_ROLE_ID,
            portrait=data.portrait,
            category_id=None,
            status=user_status,
            is_verified=data.is_verified,
            verification_token=data.verification_token,
            verification_expires_at=data.verification_expires_at,
        )

        self.db.add(user_orm)
        self.db.commit()
        self.db.refresh(user_orm)
        return UserResponseDTO.from_orm(user_orm)

    def get_by_verification_token(self, token: str) -> UserDTO | None:
        user = self.db.query(User).filter(User.verification_token == token).first()
        return UserDTO.from_orm(user) if user else None

    def get_by_id(self, user_id: int) -> UserResponseDTO | None:
        user = self.db.query(User).filter(User.id == user_id).first()
        return UserResponseDTO.from_orm(user) if user else None

    def confirm_email_verification(self, user_id: int) -> None:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return

        user.is_verified = True
        user.verification_token = None
        user.verification_expires_at = None

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)