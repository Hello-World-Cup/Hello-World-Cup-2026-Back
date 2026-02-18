from pydantic.generics import GenericModel # type: ignore
from typing import Generic, TypeVar, Optional


T=TypeVar("T")

class ResultSchema(GenericModel, Generic[T]):
    success: bool
    status_code: str
    error: Optional[str]
    data: Optional[T]

class ResponseFormatter:
    @staticmethod
    def format_response(success: bool=True, status_code: str="REQUEST_COMPLETED", error: str | None=None, data: dict | None=None) -> dict:
        return ResultSchema(
            success=success,
            status_code=status_code,
            error=error,
            data=data
        )
