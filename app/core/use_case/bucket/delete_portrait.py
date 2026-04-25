from app.domain.exceptions.base_exceptions import DomainException
from app.domain.exceptions.error_codes import USER_UNAUTHORIZED
from app.ports.driving.storage_bucket_interfaz import StorageBucketInterfaceABC
from app.ports.driving.handler_interface import HandlerInterface
from app.domain.dtos.bucket_dto import DeletePortraitDTO
from app.adapters.routing.utils.context import user_context


class DeletePortraitHandler(HandlerInterface):
    def __init__(self, storage: StorageBucketInterfaceABC) -> None:
        self._storage = storage
    
    async def execute(self, dto: DeletePortraitDTO) -> dict:
        user = user_context.get()

        if not user or not user.id:
            raise DomainException("Authentication required", USER_UNAUTHORIZED)

        if not user.id == int(dto.user_id):
            raise DomainException(
                "Unauthorized to upload portrait for this user", USER_UNAUTHORIZED
            )

        path = f"portrait/user_{dto.user_id}.png"
        
        await self._storage.delete_file("images", path)

        return {
            "path": path,
            "message": "Profile picture deleted successfully"
        }