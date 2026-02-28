from abc import ABC, abstractmethod
from io import BytesIO


class StorageBucketInterfaceABC(ABC):    
    @abstractmethod
    async def upload_file(self, bucket: str, path: str, file_data: BytesIO, content_type: str) -> str:
        raise NotImplementedError("Upload file method not implemented")
    
    @abstractmethod
    async def get_public_url(self, bucket: str, path: str) -> str:
        raise NotImplementedError("Get public URL method not implemented")
    
    @abstractmethod
    async def get_signed_url(self, bucket: str, path: str, expires_in: int = 3600) -> str:
        raise NotImplementedError("Get signed URL method not implemented")
    
    @abstractmethod
    async def delete_file(self, bucket: str, path: str) -> bool:
        raise NotImplementedError("Delete file method not implemented")
    
