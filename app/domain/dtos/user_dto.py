from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field  # type: ignore

from app.domain.enums import UserStatus


class LoginInputDTO(BaseModel):
    name: str = Field(..., min_length=1)
    email: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


class LoginResponseDTO(BaseModel):
    access_token: str = Field(...)
    refresh_token: str = Field(...)
    token_type: str = Field(default="bearer")
    user: "UserResponseDTO" = Field(...)


class SignOutResponseDTO(BaseModel):
    message: str = Field(default="Session closed successfully")


class RegisterUserInputDTO(BaseModel):
    name: str = Field(..., min_length=1)
    email: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)
    portrait: str | None = Field(default=None)
    status: UserStatus | None = Field(default=None)


class CreateUserDTO(BaseModel):
    name: str
    email: str
    password_hash: str
    portrait: str | None = None
    status: UserStatus | None = None
    verification_token: str | None = None
    verification_expires_at: datetime | None = None
    is_verified: bool = False


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
    is_verified: bool | None = Field(default=None)
    verification_token: str | None = Field(default=None)
    verification_expires_at: datetime | None = Field(default=None)

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
            is_verified=getattr(orm_obj, "is_verified", None),
            verification_token=getattr(orm_obj, "verification_token", None),
            verification_expires_at=getattr(orm_obj, "verification_expires_at", None),
        )


class UserResponseDTO(BaseModel):
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


class RefreshTokenInputDTO(BaseModel):
    refresh_token: str = Field(..., min_length=20)


class RefreshTokenResponseDTO(BaseModel):
    access_token: str = Field(...)
    refresh_token: str = Field(...)
    token_type: str = Field(default="bearer")


class SignOutInputDTO(BaseModel):
    refresh_token: str = Field(..., min_length=20)