from pydantic import BaseModel, Field  # type: ignore
from app.domain.enums import UserStatus


class RegisterUserInputDTO(BaseModel):
    """DTO para el body del request de registro."""

    name: str = Field(..., min_length=1)
    email: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)
    portrait: str | None = Field(default=None)
    status: UserStatus | None = Field(default=None)


class UserDTO(BaseModel):
    id: int | None = Field(default=None)
    username: str | None = Field(default=None)
    role_id: int | None = Field(default=None)
    name: str | None = Field(default=None)
    email: str | None = Field(default=None)
    password_hash: str | None = Field(default=None)
    portrait: str | None = Field(default=None)
    status: UserStatus | None = Field(default=None)
    category_id: int | None = Field(default=None)

    @classmethod
    def from_orm(cls, orm_obj: object) -> "UserDTO":
        return cls(
            id=getattr(orm_obj, "id", None),
            username=getattr(orm_obj, "username", None),
            role_id=getattr(orm_obj, "role_id", None),
            name=getattr(orm_obj, "name", None),
            email=getattr(orm_obj, "email", None),
            password_hash=getattr(orm_obj, "password_hash", None),
            portrait=getattr(orm_obj, "portrait", None),
            status=getattr(orm_obj, "status", None),
            category_id=getattr(orm_obj, "category_id", None),
        )


class UserResponseDTO(BaseModel):
    """DTO para la respuesta del registro (sin password_hash)."""

    id: int | None = Field(default=None)
    username: str | None = Field(default=None)
    role_id: int | None = Field(default=None)
    name: str | None = Field(default=None)
    email: str | None = Field(default=None)
    portrait: str | None = Field(default=None)
    status: UserStatus | None = Field(default=None)
    category_id: int | None = Field(default=None)

    @classmethod
    def from_orm(cls, orm_obj: object) -> "UserResponseDTO":
        return cls(
            id=getattr(orm_obj, "id", None),
            username=getattr(orm_obj, "username", None),
            role_id=getattr(orm_obj, "role_id", None),
            name=getattr(orm_obj, "name", None),
            email=getattr(orm_obj, "email", None),
            portrait=getattr(orm_obj, "portrait", None),
            status=getattr(orm_obj, "status", None),
            category_id=getattr(orm_obj, "category_id", None),
        )
