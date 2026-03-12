from app.domain.exceptions.error_codes import (
    BASE_EXCEPTION,
    RECORD_NOT_FOUND_EXCEPTION,
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

class BucketException(Exception):
    pass

class InvalidFileTypeError(BucketException):
    def __init__(self, expected: str, received: str, field: str):
        self.expected = expected
        self.received = received
        self.field = field
        super().__init__(f"Tipo de archivo inválido para {field}. Esperado: {expected}, recibido: {received}")

class FileSizeExceededError(BucketException):
    def __init__(self, max_size_mb: float, actual_size_mb: float, field: str):
        self.max_size_mb = max_size_mb
        self.actual_size_mb = actual_size_mb
        self.field = field
        super().__init__(
            f"Tamaño excedido para {field}. Máximo: {max_size_mb} MB, actual: {actual_size_mb:.2f} MB"
        )

class FileNotFoundError(BucketException):
    def __init__(self, bucket: str, path: str, message: str = "Archivo no encontrado"):
        self.bucket = bucket
        self.path = path
        super().__init__(f"{message} (bucket: {bucket}, path: {path})")

class BucketNotFoundError(BucketException):
    def __init__(self, bucket: str):
        self.bucket = bucket
        super().__init__(f"Bucket '{bucket}' no configurado")

