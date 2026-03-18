from typing import Any

from fastapi import APIRouter, Depends, Query

from app.adapters.database.dependencies import (
    get_register_user_handler,
    get_login_user_handler,
    get_refresh_access_token_handler,
    get_signout_handler,
    get_current_user_payload,
    get_current_user_handler,
    get_verify_email_handler,
)
from app.adapters.routing.utils.decorators import format_response
from app.adapters.routing.utils.response import ResultSchema
from app.domain.dtos.user_dto import (
    RegisterUserInputDTO,
    UserResponseDTO,
    LoginInputDTO,
    LoginResponseDTO,
    RefreshTokenInputDTO,
    RefreshTokenResponseDTO,
    SignOutInputDTO,
    SignOutResponseDTO,
)
from app.domain.exceptions.base_exceptions import UnauthorizedException
from app.ports.driving.handler_interface import HandlerInterface

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



@router.post("/refresh", response_model=ResultSchema[RefreshTokenResponseDTO])
@format_response
def refresh(
    data: RefreshTokenInputDTO,
    use_case: HandlerInterface = Depends(get_refresh_access_token_handler),
) -> Any:
    return use_case.execute(data)


@router.post("/signout", response_model=ResultSchema[SignOutResponseDTO])
@format_response
def signout(
    data: SignOutInputDTO,
    use_case: HandlerInterface = Depends(get_signout_handler),
) -> Any:
    return use_case.execute(data)


@router.get("/me", response_model=ResultSchema[UserResponseDTO])
@format_response
def me(
    payload: dict = Depends(get_current_user_payload),
    use_case: HandlerInterface = Depends(get_current_user_handler),
) -> Any:
    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedException("Invalid token: missing sub")

    return use_case.execute(int(user_id))


@router.get("/verify", response_model=ResultSchema[dict])
@format_response
def verify_email(
    token: str = Query(..., min_length=10),
    use_case: HandlerInterface = Depends(get_verify_email_handler),
) -> Any:
    return use_case.execute(token)