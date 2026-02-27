from datetime import datetime, timezone
from typing import Any
from app.adapters.database.postgres.repositories.user_repository import UserRepository
from fastapi import APIRouter, Depends, Query
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

@router.get("/verify", response_model=ResultSchema[dict])
@format_response
def verify_email(
    token: str = Query(..., min_length=10),
    db: Session = Depends(get_db),
) -> Any:
    user = UserRepository(db).get_by_verification_token(token)
    if not user or not user.verification_expires_at:
        raise UnauthorizedException("Invalid or expired verification token")

    now = datetime.now(timezone.utc)
    expires_at = user.verification_expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if expires_at < now:
        raise UnauthorizedException("Invalid or expired verification token")

    user.is_verified = True
    user.verification_token = None
    user.verification_expires_at = None

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "Email verified successfully"}
