from app.ports.driving.storage_bucket_interfaz import StorageBucketInterfaceABC
from app.ports.driving.handler_interface import HandlerInterface
from app.domain.dtos.bucket_dto import UploadExerciseDTO
from app.domain.exceptions.base_exceptions import (
    InvalidFileTypeError,
    FileSizeExceededError,
    BucketNotFoundError
)
from io import BytesIO


class UploadExerciseHandler(HandlerInterface):
    MAX_FILE_SIZE = 20 * 1024 * 1024  
    
    def __init__(self, storage: StorageBucketInterfaceABC):
        self._storage = storage
    
    def execute(self, dto: UploadExerciseDTO) -> dict:
        if dto.content_type != "application/pdf":
            raise InvalidFileTypeError(
                expected="application/pdf",
                received=dto.content_type,
                field="exercise"
            )
        
        dto.file_data.seek(0)
        file_bytes = dto.file_data.read()
        if len(file_bytes) > self.MAX_FILE_SIZE:
            raise FileSizeExceededError(
                max_size_mb=self.MAX_FILE_SIZE / (1024 * 1024),
                actual_size_mb=len(file_bytes) / (1024 * 1024),
                field="exercise"
            )
        
        path = f"exercise_{dto.exercise_id}.pdf"
        
        try:
            url = self._storage.upload_file(
                bucket="exercises",
                path=path,
                file_data=BytesIO(file_bytes),
                content_type="application/pdf"
            )
            return {
                "url": url,
                "path": path,
                "expires_in": 3600
            }
        except ValueError as e:
            if "Bucket" in str(e) and "no configurado" in str(e):
                raise BucketNotFoundError(bucket="exercises")
            raise