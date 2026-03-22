from typing import Any

from fastapi import APIRouter, Depends, Query # type: ignore

from app.adapters.database.dependencies import (
    RequireRoles,
    get_register_user_handler,
    get_login_user_handler,
    get_refresh_access_token_handler,
    get_signout_handler,
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
from app.ports.driving.handler_interface import HandlerInterface

from app.adapters.routing.utils.context import user_context


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
def me(_=Depends(RequireRoles([], []))) -> Any:
    return user_context.get()


@router.get("/verify", response_model=ResultSchema[dict])
@format_response
def verify_email(
    token: str = Query(..., min_length=10),
    use_case: HandlerInterface = Depends(get_verify_email_handler),
) -> Any:
    return use_case.execute(token)