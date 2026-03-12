from app.ports.driving.storage_bucket_interfaz import StorageBucketInterfaceABC
from app.ports.driving.handler_interface import HandlerInterface
from app.domain.dtos.bucket_dto import DeletePortraitDTO
from app.domain.exceptions.base_exceptions import (
    FileNotFoundError,
)


class DeletePortraitHandler(HandlerInterface):
    def __init__(self, storage: StorageBucketInterfaceABC):
        self._storage = storage
    
    def execute(self, dto: DeletePortraitDTO) -> dict:

        path = f"portrait/user_{dto.user_id}.png"
        
        exists = self._storage.file_exists("images", path)
        if not exists:
            raise FileNotFoundError(
                bucket="images",
                path=path,
                message="No existe foto de perfil para este usuario"
            )
        
        deleted = self._storage.delete_file("images", path)
        if not deleted:
            raise FileNotFoundError(
                bucket="images",
                path=path,
                message="Error al eliminar la foto de perfil"
            )
        
        return {
            "path": path,
            "message": "Foto de perfil eliminada exitosamente"
        }