from app.ports.driving.storage_bucket_interfaz import StorageBucketInterfaceABC
from app.ports.driving.handler_interface import HandlerInterface
from app.domain.dtos.bucket_dto import GetPortraitDTO

class GetPortraitHandler(HandlerInterface):
    def __init__(self, storage: StorageBucketInterfaceABC):
        self._storage = storage
    
    async def execute(self, dto: GetPortraitDTO) -> dict:
        path = f"portrait/user_{dto.user_id}.png"
        url = await self._storage.get_signed_url(
            bucket="images",
            path=path,
            expires_in=3600
        )
        return {
            "url": url,
            "expires_in": 3600,
            "message": "Portrait URL retrieved successfully"
        }