from app.ports.driving.storage_bucket_interfaz import StorageBucketInterfaceABC
from app.ports.driving.handler_interface import HandlerInterface
from app.domain.dtos.bucket_dto import GetExerciseDTO


class GetExerciseHandler(HandlerInterface):
    def __init__(self, storage: StorageBucketInterfaceABC):
        self._storage = storage

    async def execute(self, dto: GetExerciseDTO) -> dict:
        path = f"exercise_{dto.exercise_id}.pdf"
        url = await self._storage.get_signed_url(
            bucket="exercises", path=path, expires_in=3600
        )
        return {
            "url": url,
            "expires_in": 3600,
            "message": "Exercise file URL retrieved successfully",
        }
