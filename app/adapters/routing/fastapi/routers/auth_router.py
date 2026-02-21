from typing import Any
from fastapi import APIRouter, Depends
from app.ports.driving.handler_interface import HandlerInterface
from app.domain.dtos.user_dto import RegisterUserInputDTO, UserResponseDTO
from app.adapters.routing.utils.response import ResultSchema
from app.adapters.routing.utils.decorators import format_response
from app.adapters.database.dependencies import get_register_user_handler

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=201, response_model=ResultSchema[UserResponseDTO])
@format_response
def register_user(
    data: RegisterUserInputDTO,
    use_case: HandlerInterface = Depends(get_register_user_handler),
) -> Any:
    return use_case.execute(data)