from app.ports.driving.storage_bucket_interfaz import StorageBucketInterfaceABC
from app.ports.driving.handler_interface import HandlerInterface
from app.domain.dtos.bucket_dto import UploadPortraitDTO
from app.domain.exceptions.base_exceptions import (
    InvalidFileTypeError,
    FileSizeExceededError,
    BucketNotFoundError
)
from io import BytesIO


class UploadPortraitHandler(HandlerInterface):
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
    
    def __init__(self, storage: StorageBucketInterfaceABC):
        self._storage = storage
    
    def execute(self, dto: UploadPortraitDTO) -> dict:

        if dto.content_type != "image/png":
            raise InvalidFileTypeError(
                expected="image/png",
                received=dto.content_type,
                field="portrait"
            )
        
        dto.file_data.seek(0)
        file_bytes = dto.file_data.read()
        if len(file_bytes) > self.MAX_FILE_SIZE:
            raise FileSizeExceededError(
                max_size_mb=self.MAX_FILE_SIZE / (1024 * 1024),
                actual_size_mb=len(file_bytes) / (1024 * 1024),
                field="portrait"
            )
        
        path = f"portrait/user_{dto.user_id}.png"
        
        try:
            url = self._storage.upload_file(
                bucket="images",
                path=path,
                file_data=BytesIO(file_bytes),
                content_type="image/png"
            )
            return {
                "url": url,
                "path": path,
                "expires_in": 3600
            }
        except ValueError as e:
            if "Bucket" in str(e) and "no configurado" in str(e):
                raise BucketNotFoundError(bucket="images")
            raise