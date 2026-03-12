from pydantic import BaseModel, Field
from typing import Optional
from io import BytesIO

class UploadPortraitDTO(BaseModel):
    user_id: str = Field(..., description="ID del usuario")
    file_data: BytesIO  # Nota: BytesIO no es serializable, lo manejamos en el handler
    content_type: str = Field(..., description="Tipo MIME del archivo")
    
    class Config:
        arbitrary_types_allowed = True

class UploadSponsorLogoDTO(BaseModel):
    sponsor_id: str = Field(..., description="ID del sponsor")
    file_data: BytesIO
    content_type: str = Field(..., description="Tipo MIME del archivo")
    
    class Config:
        arbitrary_types_allowed = True

class UploadExerciseDTO(BaseModel):
    exercise_id: str = Field(..., description="ID del ejercicio")
    file_data: BytesIO
    content_type: str = Field(..., description="Tipo MIME del archivo")
    
    class Config:
        arbitrary_types_allowed = True

class DeletePortraitDTO(BaseModel):
    user_id: str = Field(..., description="ID del usuario")

class DeleteSponsorLogoDTO(BaseModel):
    sponsor_id: str = Field(..., description="ID del sponsor")

class DeleteExerciseDTO(BaseModel):
    exercise_id: str = Field(..., description="ID del ejercicio")