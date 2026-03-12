from io import BytesIO
from app.ports.driving.storage_bucket_interfaz import StorageBucketInterfaceABC
from app.domain.exceptions.base_exceptions import (
    BucketNotFoundError,
    FileNotFoundError,
    InvalidFileTypeError,
)


class StorageBucketSupabase(StorageBucketInterfaceABC):

    BUCKET_CONFIG = {
        "images": {"allowed_types": ["image/png"]},
        "exercises": {"allowed_types": ["application/pdf"]}
    }
    
    def __init__(self, supabase_client):
        self.supabase_client = supabase_client
    
    async def upload_file(self, bucket: str, path: str, file_data: BytesIO, content_type: str) -> str:
        if bucket not in self.BUCKET_CONFIG:
            raise BucketNotFoundError(bucket=bucket) 
        
        if content_type not in self.BUCKET_CONFIG[bucket]["allowed_types"]:
            raise InvalidFileTypeError(
            expected=", ".join(self.BUCKET_CONFIG[bucket]["allowed_types"]),
            received=content_type,
            field="file"
            )  
        
        try:
            file_data.seek(0)
            self.supabase_client.storage.from_(bucket).upload(
                path=path,
                file=file_data.read(),
                file_options={"content-type": content_type}
            )
            return await self.get_signed_url(bucket, path)
        except Exception as e:
            error_msg = str(e).lower()
            if "404" in error_msg or "not found" in error_msg:
                raise FileNotFoundError(bucket=bucket, path=path) from e 
            if "bucket" in error_msg and "not found" in error_msg:
                raise BucketNotFoundError(bucket=bucket) from e 
            raise
        
    async def get_public_url(self, bucket: str, path: str) -> str: #revisar si admite null o none
        return self.supabase_client.storage.from_(bucket).get_public_url(path)
    
    async def get_signed_url(self, bucket: str, path: str, expires_in: int = 3600) -> str:
        try:
            response = self.supabase_client.storage.from_(bucket).create_signed_url(
                path=path,
                expires_in=expires_in
            )
            return response.get("signedURL") or response.get("signedUrl")
        except Exception as e:
            error_msg = str(e).lower()
            if "404" in error_msg or "not found" in error_msg:
                raise FileNotFoundError(bucket=bucket, path=path) from e
            if "bucket" in error_msg and "not found" in error_msg:
                raise BucketNotFoundError(bucket=bucket) from e
            raise
    
    async def delete_file(self, bucket: str, path: str) -> bool:

        if bucket not in self.BUCKET_CONFIG:
            raise BucketNotFoundError(bucket=bucket)
        
        try:
            response = self.supabase_client.storage.from_(bucket).remove([path])
            
            if isinstance(response, list) and len(response) > 0:
                result = response[0]
                if isinstance(result, dict) and result.get("error"):
                    error_msg = str(result["error"]).lower()
                    if "404" in error_msg or "not found" in error_msg:
                        raise FileNotFoundError(bucket=bucket, path=path)
                    if "bucket" in error_msg and "not found" in error_msg:
                        raise BucketNotFoundError(bucket=bucket)
            return True
            
        except Exception as e:
            error_msg = str(e).lower()
            if "404" in error_msg or "not found" in error_msg:
                raise FileNotFoundError(bucket=bucket, path=path) from e
            if "bucket" in error_msg and "not found" in error_msg:
                raise BucketNotFoundError(bucket=bucket) from e
            raise