from app.domain.exceptions.error_codes import (
    BASE_EXCEPTION,
    RECORD_NOT_FOUND_EXCEPTION,
)

class DomainException(Exception):
    def __init__(self, message: str, error_code: str = BASE_EXCEPTION) -> None:
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

class RecordNotFoundException(DomainException):
    def __init__(self, model: str) -> None:
        self.model = model
        error_code = (
            f"{RECORD_NOT_FOUND_EXCEPTION}.{model.upper()}"
            if model
            else RECORD_NOT_FOUND_EXCEPTION
        )
        super().__init__(f"Record not found for model '{model}'", error_code)