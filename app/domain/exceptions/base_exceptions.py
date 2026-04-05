from app.domain.exceptions.error_codes import (
    BASE_EXCEPTION,
    RECORD_NOT_FOUND_EXCEPTION,
    INVALID_FILE_TYPE,
    FILE_SIZE_EXCEEDED,
    FILE_NOT_FOUND,
    BUCKET_NOT_FOUND,
    DUPLICATE_RECORD_EXCEPTION,
    INVALID_CREDENTIALS_EXCEPTION,
    UNAUTHORIZED_EXCEPTION,
    FORBIDDEN_EXCEPTION,
    TEAM_EXCEPTION,
    TEAM_NOT_FOUND,
    TEAM_NO_CURRENT_EDITION,
    TEAM_NO_ASSOCIATION,
    USER_EXCEPTION,
    USER_NOT_FOUND,
    USER_UNAUTHORIZED,
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


class BucketException(Exception):
    pass


class InvalidFileTypeError(BucketException):
    def __init__(self, expected: str, received: str, field: str = "file"):
        message = (
            f"Invalid file type for {field}. Expected: {expected}, received: {received}"
        )
        super().__init__(message, INVALID_FILE_TYPE)
        self.expected = expected
        self.received = received
        self.field = field

class FileSizeExceededError(BucketException):
    def __init__(self, max_size_mb: float, actual_size_mb: float, field: str = "file"):
        message = f"File size exceeded for {field}. Maximum: {max_size_mb} MB, actual: {actual_size_mb:.2f} MB"
        super().__init__(message, FILE_SIZE_EXCEEDED)
        self.max_size_mb = max_size_mb
        self.actual_size_mb = actual_size_mb
        self.field = field

class FileNotFoundError(BucketException):
    def __init__(self, bucket: str, path: str, message: str = "File not found"):
        super().__init__(message, FILE_NOT_FOUND)
        self.bucket = bucket
        self.path = path
        
class BucketNotFoundError(BucketException):
    def __init__(self, bucket: str):
        message = f"Bucket '{bucket}' is not configured or does not exist"
        super().__init__(message, BUCKET_NOT_FOUND)
        self.bucket = bucket


class DuplicateRecordException(DomainException):
    def __init__(self, message: str, field: str = "") -> None:
        error_code = (
            f"{DUPLICATE_RECORD_EXCEPTION}.{field.upper()}"
            if field
            else DUPLICATE_RECORD_EXCEPTION
        )
        super().__init__(message, error_code)

class InvalidCredentialsException(DomainException):
    def __init__(self, message: str = "Invalid credentials", field: str = "") -> None:
        error_code = (
            f"{INVALID_CREDENTIALS_EXCEPTION}.{field.upper()}"
            if field
            else INVALID_CREDENTIALS_EXCEPTION
        )
        super().__init__(message, error_code)

class UnauthorizedException(DomainException):
    def __init__(self, message: str = "Invalid or expired session") -> None:
        super().__init__(message, UNAUTHORIZED_EXCEPTION)


class ForbiddenException(DomainException):
    def __init__(
        self, message: str = "You are not allowed to perform this action"
    ) -> None:
        super().__init__(message, FORBIDDEN_EXCEPTION)


class TeamException(DomainException):
    def __init__(self, message: str, error_code: str = TEAM_EXCEPTION) -> None:
        super().__init__(message, error_code)


class TeamNotFoundException(TeamException):
    def __init__(self, user_id: str) -> None:
        message = f"Team not found for user '{user_id}'"
        super().__init__(message, TEAM_NOT_FOUND)
        self.user_id = user_id


class NoCurrentEditionException(TeamException):
    def __init__(self) -> None:
        message = "No current edition found"
        super().__init__(message, TEAM_NO_CURRENT_EDITION)


class NoTeamAssociationException(TeamException):
    def __init__(self, user_id: str) -> None:
        message = f"No team association found for user '{user_id}'"
        super().__init__(message, TEAM_NO_ASSOCIATION)
        self.user_id = user_id


class UserException(DomainException):
    def __init__(self, message: str, error_code: str = USER_EXCEPTION) -> None:
        super().__init__(message, error_code)


class UserNotFoundException(UserException):
    def __init__(self, user_id: str) -> None:
        message = f"User not found: '{user_id}'"
        super().__init__(message, USER_NOT_FOUND)
        self.user_id = user_id