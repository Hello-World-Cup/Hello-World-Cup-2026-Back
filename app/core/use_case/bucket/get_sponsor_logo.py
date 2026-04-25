from app.ports.driving.storage_bucket_interfaz import StorageBucketInterfaceABC
from app.ports.driving.handler_interface import HandlerInterface
from app.domain.dtos.bucket_dto import GetSponsorLogoDTO


class GetSponsorLogoHandler(HandlerInterface):
    def __init__(self, storage: StorageBucketInterfaceABC):
        self._storage = storage

    async def execute(self, dto: GetSponsorLogoDTO) -> dict:
        path = f"sponsors/sponsor_{dto.sponsor_id}.png"
        url = await self._storage.get_signed_url(
            bucket="images", path=path, expires_in=3600
        )
        return {
            "url": url,
            "expires_in": 3600,
            "message": "Sponsor logo URL retrieved successfully",
        }
