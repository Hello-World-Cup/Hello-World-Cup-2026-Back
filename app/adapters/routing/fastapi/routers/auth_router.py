from typing import Any
from app.adapters.database.postgres.repositories.user_repository import UserRepository
from fastapi import APIRouter, Depends
from app.ports.driving.handler_interface import HandlerInterface
from app.domain.dtos.user_dto import (
    RegisterUserInputDTO,
    UserResponseDTO,
    LoginInputDTO,
    LoginResponseDTO,
    SignOutResponseDTO,
)
from app.adapters.routing.utils.response import ResultSchema
from app.adapters.routing.utils.decorators import format_response
from app.adapters.database.dependencies import (
    get_register_user_handler,
    get_login_user_handler,
    get_current_user_payload,
    get_db
)
from app.domain.exceptions.base_exceptions import UnauthorizedException
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=201, response_model=ResultSchema[UserResponseDTO])
@format_response
def register_user(
    data: RegisterUserInputDTO,
    use_case: HandlerInterface = Depends(get_register_user_handler),
) -> Any:
    return use_case.execute(data)


@router.post("/login", response_model=ResultSchema[LoginResponseDTO])
@format_response
def login(
    data: LoginInputDTO,
    use_case: HandlerInterface = Depends(get_login_user_handler),
) -> Any:
    return use_case.execute(data)


@router.post("/signout", response_model=ResultSchema[SignOutResponseDTO])
@format_response
def signout(
    _payload: dict = Depends(get_current_user_payload),
) -> Any:
    """Cierra la sesión. Solo funciona si el usuario tiene un token JWT válido (sesión activa)."""
    return SignOutResponseDTO()

@router.get("/me", response_model=ResultSchema[UserResponseDTO])
@format_response
def me(payload:dict=Depends(get_current_user_payload),db:Session=Depends(get_db))->Any:
    email= payload.get("email")
    if not email:
        raise UnauthorizedException("Token inválido: falta email")

    user = UserRepository(db).get_by_email(email)
    if not user: 
        raise UnauthorizedException("Usuario no existe o sesión inválida")
    
    return UserResponseDTO.from_orm(user)