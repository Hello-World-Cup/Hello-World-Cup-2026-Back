from app.ports.driving.storage_bucket_interfaz import StorageBucketInterfaceABC
from app.ports.driving.handler_interface import HandlerInterface
from app.domain.dtos.bucket_dto import DeletePortraitDTO
from app.domain.exceptions.base_exceptions import FileNotFoundError  # ← Import desde dominio

class DeletePortraitHandler(HandlerInterface):
    def __init__(self, storage: StorageBucketInterfaceABC):
        self._storage = storage
    
    async def execute(self, dto: DeletePortraitDTO) -> dict:
        path = f"portrait/user_{dto.user_id}.png"
        
        await self._storage.delete_file("images", path)

        return {
            "path": path,
            "message": "Profile picture deleted successfully"  # ← Inglés
        }