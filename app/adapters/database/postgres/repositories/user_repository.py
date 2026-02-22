from sqlalchemy import func
from sqlalchemy.orm import Session

from app.adapters.database.postgres.models.user_model import User
from app.ports.driven.database.postgres.user_repository_abc import UserRepositoryInterface
from app.domain.dtos.user_dto import UserResponseDTO
from app.domain.enums import UserStatus
from app.domain.exceptions.base_exceptions import DuplicateRecordException


class UserRepository(UserRepositoryInterface):
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_email(self, email: str):
        email_normalized = email.strip().lower()
        return self.db.query(User).filter(func.lower(User.email) == email_normalized).first()

    def create(
        self,
        name: str,
        email: str,
        password_hash: str,
        portrait: str | None = None,
        status: UserStatus | None = None,
    ) -> UserResponseDTO:
        if self.db.query(User).filter(User.email == email).first():
            raise DuplicateRecordException(
                f"Ya existe un usuario con el email '{email}'", field="EMAIL"
            )

        # username derivado del email (parte antes de @)
        username = email.split("@")[0]
        if self.db.query(User).filter(User.username == username).first():
            raise DuplicateRecordException(
                f"Ya existe un usuario con el username '{username}'", field="USERNAME"
            )

        user_status = status if status is not None else UserStatus.PENDING
        DEFAULT_ROLE_ID = 2

        user_orm = User(
            username=username,
            name=name,
            email=email,
            password_hash=password_hash,
            role_id=DEFAULT_ROLE_ID,
            portrait=portrait,
            category_id=None,
            status=user_status,
        )
        self.db.add(user_orm)
        self.db.commit()
        self.db.refresh(user_orm)
        return UserResponseDTO.from_orm(user_orm)
