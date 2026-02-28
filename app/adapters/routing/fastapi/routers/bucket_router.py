# app/adapters/routing/routers/bucket_router.py

from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException, Path
from io import BytesIO
from app.ports.driving.storage_bucket_interfaz import StorageBucketInterfaceABC
from app.adapters.database.dependencies import get_storage
from app.adapters.routing.utils.decorators import format_response
from app.adapters.routing.utils.response import ResultSchema

bucket_router = APIRouter(tags=["bucket"])


@bucket_router.post("/portrait")
@format_response
async def upload_portrait(
    file: UploadFile = File(...),
    user_id: str = Form(...),
    storage: StorageBucketInterfaceABC = Depends(get_storage)
) -> ResultSchema:
    if file.content_type != "image/png":
        raise HTTPException(400, "Solo PNG permitido")
    
    content = await file.read()
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(400, "Máximo 5 MB")
    
    path = f"portrait/user_{user_id}.png"
    
    try:
        url = await storage.upload_file(
            bucket="images",  
            path=path,
            file_data=BytesIO(content),
            content_type="image/png"
        )
        
        return ResultSchema(
            success=True,
            status_code="200",  
            error=None,         
            message="Foto de perfil subida",
            data={"url": url, "expires_in": 3600}
        )
        
    except Exception as e:
        return ResultSchema(
            success=False,
            status_code="500",
            error=str(e),
            message="Error al subir foto de perfil",
            data=None
        )

@bucket_router.post("/sponsors/logo")
@format_response
async def upload_sponsor_logo(
    file: UploadFile = File(...),
    sponsor_id: str = Form(...),
    storage: StorageBucketInterfaceABC = Depends(get_storage)
) -> ResultSchema:
    if file.content_type != "image/png":
        raise HTTPException(400, "Solo PNG permitido")
    
    content = await file.read()
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(400, "Máximo 10 MB")
    
    path = f"sponsors/sponsor_{sponsor_id}.png"
    
    try:
        url = await storage.upload_file(
            bucket="images", 
            path=path,
            file_data=BytesIO(content),
            content_type="image/png"
        )
        
        return ResultSchema(
            success=True,
            status_code="200",  
            error=None,        
            message="Logo de sponsor subido",
            data={"url": url, "expires_in": 3600}
        )
        
    except Exception as e:
        return ResultSchema(
            success=False,
            status_code="500",
            error=str(e),
            message="Error al subir logo de sponsor",
            data=None
        )

@bucket_router.post("/exercises/upload")
@format_response
async def upload_exercise(
    file: UploadFile = File(...),
    exercise_id: str = Form(...),
    storage: StorageBucketInterfaceABC = Depends(get_storage)
) -> ResultSchema:
    if file.content_type != "application/pdf":
        raise HTTPException(400, "Solo PDF permitido")
    
    content = await file.read()
    if len(content) > 20 * 1024 * 1024:
        raise HTTPException(400, "Máximo 20 MB")
    
    path = f"exercise_{exercise_id}.pdf"
    
    try:
        url = await storage.upload_file(
            bucket="exercises",  
            path=path,
            file_data=BytesIO(content),
            content_type="application/pdf"
        )
        
        return ResultSchema(
            success=True,
            status_code="200",  
            error=None,         
            message="Ejercicio subido",
            data={"url": url, "expires_in": 3600}
        )
        
    except Exception as e:
        return ResultSchema(
            success=False,
            status_code="500",
            error=str(e),
            message="Error al subir ejercicio",
            data=None
        )
    
@bucket_router.delete("/portrait/{user_id}")
@format_response
async def delete_portrait(
    user_id: str = Path(..., description="ID del usuario"),
    storage: StorageBucketInterfaceABC = Depends(get_storage)
) -> ResultSchema:
    path = f"portrait/user_{user_id}.png"
    
    try:
        exists = await storage.file_exists("images", path)
        if not exists:
            return ResultSchema(
                success=False,
                status_code="404",
                error="Foto no encontrada",
                message="No existe foto de perfil para este usuario",
                data=None
            )
        
        deleted = await storage.delete_file("images", path)
        
        if deleted:
            return ResultSchema(
                success=True,
                status_code="200",
                error=None,
                message="Foto de perfil eliminada exitosamente",
                data={"path": path}
            )
        else:
            return ResultSchema(
                success=False,
                status_code="404",
                error="Foto no encontrada",
                message="La foto de perfil no existe",
                data=None
            )
            
    except Exception as e:
        return ResultSchema(
            success=False,
            status_code="500",
            error=str(e),
            message="Error al eliminar foto de perfil",
            data=None
        )

@bucket_router.delete("/sponsors/{sponsor_id}/logo")
@format_response
async def delete_sponsor_logo(
    sponsor_id: str = Path(..., description="ID del sponsor"),
    storage: StorageBucketInterfaceABC = Depends(get_storage)
) -> ResultSchema:
    path = f"sponsors/sponsor_{sponsor_id}.png"
    
    try:
        exists = await storage.file_exists("images", path)
        if not exists:
            return ResultSchema(
                success=False,
                status_code="404",
                error="Logo no encontrado",
                message="No existe logo para este sponsor",
                data=None
            )
        
        deleted = await storage.delete_file("images", path)
        
        if deleted:
            return ResultSchema(
                success=True,
                status_code="200",
                error=None,
                message="Logo de sponsor eliminado exitosamente",
                data={"path": path}
            )
        else:
            return ResultSchema(
                success=False,
                status_code="404",
                error="Logo no encontrado",
                message="El logo del sponsor no existe",
                data=None
            )
            
    except Exception as e:
        return ResultSchema(
            success=False,
            status_code="500",
            error=str(e),
            message="Error al eliminar logo de sponsor",
            data=None
        )

@bucket_router.delete("/exercises/{exercise_id}")
@format_response
async def delete_exercise(
    exercise_id: str = Path(..., description="ID del ejercicio"),
    storage: StorageBucketInterfaceABC = Depends(get_storage)
) -> ResultSchema:
    path = f"exercise_{exercise_id}.pdf"
    
    try:
        exists = await storage.file_exists("exercises", path)
        if not exists:
            return ResultSchema(
                success=False,
                status_code="404",
                error="Ejercicio no encontrado",
                message="No existe ejercicio con este ID",
                data=None
            )
        
        deleted = await storage.delete_file("exercises", path)
        
        if deleted:
            return ResultSchema(
                success=True,
                status_code="200",
                error=None,
                message="Ejercicio eliminado exitosamente",
                data={"path": path}
            )
        else:
            return ResultSchema(
                success=False,
                status_code="404",
                error="Ejercicio no encontrado",
                message="El ejercicio no existe",
                data=None
            )
            
    except Exception as e:
        return ResultSchema(
            success=False,
            status_code="500",
            error=str(e),
            message="Error al eliminar ejercicio",
            data=None
        )  