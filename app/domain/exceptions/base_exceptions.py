from app.domain.exceptions.error_codes import (
    BASE_EXCEPTION,
    RECORD_NOT_FOUND_EXCEPTION,
    DUPLICATE_RECORD_EXCEPTION,
    INVALID_CREDENTIALS_EXCEPTION,
    UNAUTHORIZED_EXCEPTION,
)


class DomainException(Exception):
    def __init__(self, message: str, error_code: str=BASE_EXCEPTION) -> None:
        self.message=message
        self.error_code=error_code
        super().__init__(self.message)

class RecordNotFoundException(DomainException):
    def __init__(self, model: str) -> None:
        self.model=model
        error_code=(
            f"{RECORD_NOT_FOUND_EXCEPTION}.{model.upper()}"
            if model
            else RECORD_NOT_FOUND_EXCEPTION
        )
        super().__init__(f"Record not found for model '{model}'", error_code)


class DuplicateRecordException(DomainException):
    def __init__(self, message: str, field: str = "") -> None:
        error_code = f"{DUPLICATE_RECORD_EXCEPTION}.{field.upper()}" if field else DUPLICATE_RECORD_EXCEPTION
        super().__init__(message, error_code)


class InvalidCredentialsException(DomainException):
    def __init__(self, message: str = "Credenciales inválidas") -> None:
        super().__init__(message, INVALID_CREDENTIALS_EXCEPTION)


class UnauthorizedException(DomainException):
    def __init__(self, message: str = "Sesión inválida o expirada") -> None:
        super().__init__(message, UNAUTHORIZED_EXCEPTION)