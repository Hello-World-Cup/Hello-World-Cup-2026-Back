from typing import Any
from app.ports.driving.handler_interface import HandlerInterface
from fastapi import APIRouter, Depends  # type: ignore

from app.adapters.database.dependencies import (
    delete_test_by_id_handler,
    get_test_by_id_handler,
)
from app.adapters.routing.utils.decorators import format_response
from app.adapters.routing.utils.response import ResultSchema
from app.domain.dtos.test_dto import TestDTO

test_router=APIRouter(prefix="/tests", tags=["test"])

@test_router.get("/test", response_model=ResultSchema[TestDTO])
@format_response
def read_test(
    id: int, use_case: HandlerInterface=Depends(get_test_by_id_handler)
) -> Any:
    return use_case.execute(id)

@test_router.delete("/delete-test")
@format_response
def delete_test(
    id: int, use_case: HandlerInterface=Depends(delete_test_by_id_handler)
) -> Any:
    return use_case.execute(id)