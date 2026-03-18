from typing import Any
from sqlalchemy.orm import Session
from jose import JWTError, jwt  # type: ignore
from fastapi import Depends, Header  # type: ignore

from app.core.use_case.test.delete_test import DeleteTestByIdHandler
from app.core.use_case.test.get_test import GetTestByIdHandler
from app.core.use_case.auth.register_user import RegisterUserHandler
from app.core.use_case.auth.login_user import LoginUserHandler
from app.core.use_case.auth.get_current_user import GetCurrentUserHandler
from app.core.use_case.auth.verify_email import VerifyEmailHandler
from app.adapters.database.postgres.repositories.test_repository import TestRepository
from app.adapters.database.postgres.repositories.user_repository import UserRepository
from app.adapters.database.postgres.connection import get_db
from app.domain.config import settings
from app.domain.exceptions.base_exceptions import UnauthorizedException


from app.adapters.database.postgres.repositories.refresh_token_repository import RefreshTokenRepository
from app.core.use_case.auth.refresh_access_token import RefreshAccessTokenHandler
from app.core.use_case.auth.signout import SignOutHandler
from app.adapters.email.gmail_smtp_sender import GmailSmtpSender


# Authorization

def get_current_user_payload(
    authorization: str | None = Header(None, alias="Authorization"),
) -> dict[str, Any]:
    """Validates the JWT from the Authorization header and returns the payload. Requires active session."""
    if not authorization or not authorization.startswith("Bearer "):
        raise UnauthorizedException("Token not sent or invalid format")
    token = authorization.removeprefix("Bearer ").strip()
    if not token:
        raise UnauthorizedException("Token not sent or invalid format")
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload
    except JWTError:
        raise UnauthorizedException("Invalid or expired session")


# TODO: Once the auth middleware injects the user into ContextVar, it will be obtained here and the role will be validated against required_rol
def get_authorized_user(required_role: str) -> None:
    pass

# Repositories

def get_test_repository(db: Session) -> TestRepository:
    return TestRepository(db)


def get_user_repository(db: Session) -> UserRepository:
    return UserRepository(db)


# Use cases

def get_test_by_id_handler(db: Session=Depends(get_db)) -> GetTestByIdHandler:
    return GetTestByIdHandler(get_test_repository(db))

def delete_test_by_id_handler(db: Session=Depends(get_db)) -> DeleteTestByIdHandler:
    return DeleteTestByIdHandler(get_test_repository(db))

def get_login_user_handler(db: Session = Depends(get_db)) -> LoginUserHandler:
    return LoginUserHandler(
        get_user_repository(db),
        get_refresh_token_repository(db),
    )

def get_refresh_token_repository(db: Session) -> RefreshTokenRepository:
    return RefreshTokenRepository(db)


def get_refresh_access_token_handler(db: Session = Depends(get_db)) -> RefreshAccessTokenHandler:
    return RefreshAccessTokenHandler(
        get_refresh_token_repository(db),
        get_user_repository(db),
    )

def get_signout_handler(db: Session = Depends(get_db)) -> SignOutHandler:
    return SignOutHandler(get_refresh_token_repository(db))

def get_email_sender() -> GmailSmtpSender:
    return GmailSmtpSender()

def get_register_user_handler(db: Session = Depends(get_db)) -> RegisterUserHandler:
    return RegisterUserHandler(
        get_user_repository(db),
        get_email_sender(),
    )


def get_current_user_handler(db: Session = Depends(get_db)) -> GetCurrentUserHandler:
    return GetCurrentUserHandler(get_user_repository(db))


def get_verify_email_handler(db: Session = Depends(get_db)) -> VerifyEmailHandler:
    return VerifyEmailHandler(get_user_repository(db))