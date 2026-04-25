from app.domain.exceptions.error_codes import USER_UNAUTHORIZED
from app.ports.driving.storage_bucket_interfaz import StorageBucketInterfaceABC
from app.ports.driving.handler_interface import HandlerInterface
from app.domain.dtos.bucket_dto import UploadPortraitDTO
from app.domain.exceptions.base_exceptions import (
    DomainException,
    InvalidFileTypeError,
    FileSizeExceededError,
)
from io import BytesIO
from app.adapters.routing.utils.context import user_context


class UploadPortraitHandler(HandlerInterface):
    MAX_FILE_SIZE = 5 * 1024 * 1024

    def __init__(
        self,
        storage: StorageBucketInterfaceABC,
    ) -> None:
        self._storage = storage

    async def execute(self, dto: UploadPortraitDTO) -> dict:
        user = user_context.get()

        if not user or not user.id:
            raise DomainException("Authentication required", USER_UNAUTHORIZED)

        if not user.id == dto.user_id:
            raise DomainException(
                "Unauthorized to upload portrait for this user", USER_UNAUTHORIZED
            )

        if dto.content_type != "image/png":
            raise InvalidFileTypeError(
                expected="image/png", received=dto.content_type, field="portrait"
            )

        dto.file_data.seek(0)
        file_bytes = dto.file_data.read()
        if len(file_bytes) > self.MAX_FILE_SIZE:
            raise FileSizeExceededError(
                max_size_mb=self.MAX_FILE_SIZE / (1024 * 1024),
                actual_size_mb=len(file_bytes) / (1024 * 1024),
                field="portrait",
            )

        path = f"portrait/user_{dto.user_id}.png"
        url = await self._storage.upload_file(
            bucket="images",
            path=path,
            file_data=BytesIO(file_bytes),
            content_type="image/png",
        )
        return {
            "url": url,
            "path": path,
            "expires_in": 3600,
            "message": "Profile picture uploaded successfully",  # ← Inglés
        }
