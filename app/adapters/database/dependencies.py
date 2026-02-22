from typing import Any
from sqlalchemy.orm import Session
from jose import JWTError, jwt  # type: ignore
from fastapi import Depends, Header  # type: ignore

from app.core.use_case.test.delete_test import DeleteTestByIdHandler
from app.core.use_case.test.get_test import GetTestByIdHandler
from app.core.use_case.auth.register_user import RegisterUserHandler
from app.core.use_case.auth.login_user import LoginUserHandler
from app.adapters.database.postgres.repositories.test_repository import TestRepository
from app.adapters.database.postgres.repositories.user_repository import UserRepository
from app.adapters.database.postgres.connection import get_db
from app.domain.config import settings
from app.domain.exceptions.base_exceptions import UnauthorizedException


# Authorization

def get_current_user_payload(
    authorization: str | None = Header(None, alias="Authorization"),
) -> dict[str, Any]:
    """Valida el JWT del header Authorization y devuelve el payload. Requiere sesión activa."""
    if not authorization or not authorization.startswith("Bearer "):
        raise UnauthorizedException("Token no enviado o formato inválido")
    token = authorization.removeprefix("Bearer ").strip()
    if not token:
        raise UnauthorizedException("Token no enviado o formato inválido")
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload
    except JWTError:
        raise UnauthorizedException("Sesión inválida o expirada")


# TODO: Una vez que el middleware de autenticación haga su trabajo e inyecte al usuario al ContextVar, se obtendrá acá y se validará que su rol concuerde con el required_rol
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


def get_register_user_handler(db: Session=Depends(get_db)) -> RegisterUserHandler:
    return RegisterUserHandler(get_user_repository(db))


def get_login_user_handler(db: Session=Depends(get_db)) -> LoginUserHandler:
    return LoginUserHandler(get_user_repository(db))

