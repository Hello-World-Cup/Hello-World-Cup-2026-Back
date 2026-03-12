from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException, Path
from io import BytesIO
from app.domain.dtos.bucket_dto import (
    UploadPortraitDTO,
    UploadSponsorLogoDTO,
    UploadExerciseDTO,
    DeletePortraitDTO,
)
from app.core.use_case.bucket.upload_portrait import UploadPortraitHandler
from app.core.use_case.bucket.delete_portrait import DeletePortraitHandler
from app.core.use_case.bucket.upload_sponsor_logo import UploadSponsorLogoHandler
from app.core.use_case.bucket.upload_exercise import UploadExerciseHandler
from app.adapters.database.dependencies import (
    get_upload_portrait_handler,
    get_delete_portrait_handler,
    get_upload_sponsor_logo_handler,
    get_upload_exercise_handler
)
from app.adapters.routing.utils.decorators import format_response
from app.adapters.routing.utils.response import ResultSchema
from app.domain.exceptions.base_exceptions import (
    InvalidFileTypeError,
    FileSizeExceededError,
    FileNotFoundError,
    BucketNotFoundError
)

from app.domain.exceptions.base_exceptions import (
    InvalidFileTypeError,
    FileSizeExceededError,
    FileNotFoundError,
    BucketNotFoundError,
)


bucket_router = APIRouter(prefix="/bucket", tags=["bucket"])


@bucket_router.post("/portrait")
@format_response
async def upload_portrait(
    file: UploadFile = File(..., description="Foto de perfil (PNG)"),
    user_id: str = Form(..., description="ID del usuario"),
    handler: UploadPortraitHandler = Depends(get_upload_portrait_handler)
) -> ResultSchema:
    try:
        content = await file.read()
        
        result = handler.execute(
            UploadPortraitDTO(
                user_id=user_id,
                file_data=BytesIO(content),
                content_type=file.content_type
            )
        )
        
        return ResultSchema(
            success=True,
            status_code="200",
            error=None,
            message="Foto de perfil subida",
            data=result
        )
        
    except InvalidFileTypeError as e:
        raise HTTPException(400, str(e))
    except FileSizeExceededError as e:
        raise HTTPException(400, str(e))
    except BucketNotFoundError as e:
        raise HTTPException(500, str(e))
    except Exception as e:
        raise HTTPException(500, f"Error al subir foto: {str(e)}")

@bucket_router.delete("/portrait/{user_id}")
@format_response
async def delete_portrait(
    user_id: str = Path(..., description="ID del usuario"),
    handler: DeletePortraitHandler = Depends(get_delete_portrait_handler)
) -> ResultSchema:
    try:
        result = handler.execute(DeletePortraitDTO(user_id=user_id))
        
        return ResultSchema(
            success=True,
            status_code="200",
            error=None,
            message=result["message"],
            data={"path": result["path"]}
        )
        
    except FileNotFoundError as e:
        raise HTTPException(404, str(e))
    except Exception as e:
        raise HTTPException(500, f"Error al eliminar foto: {str(e)}")


@bucket_router.post("/sponsors/logo")
@format_response
async def upload_sponsor_logo(
    file: UploadFile = File(..., description="Logo del sponsor (PNG)"),
    sponsor_id: str = Form(..., description="ID del sponsor"),
    handler: UploadSponsorLogoHandler = Depends(get_upload_sponsor_logo_handler)
) -> ResultSchema:
    try:
        content = await file.read()
        
        result = handler.execute(
            UploadSponsorLogoDTO(
                sponsor_id=sponsor_id,
                file_data=BytesIO(content),
                content_type=file.content_type
            )
        )
        
        return ResultSchema(
            success=True,
            status_code="200",
            error=None,
            message="Logo de sponsor subido",
            data=result
        )
        
    except InvalidFileTypeError as e:
        raise HTTPException(400, str(e))
    except FileSizeExceededError as e:
        raise HTTPException(400, str(e))
    except BucketNotFoundError as e:
        raise HTTPException(500, str(e))
    except Exception as e:
        raise HTTPException(500, f"Error al subir logo: {str(e)}")

@bucket_router.post("/exercises/upload")
@format_response
async def upload_exercise(
    file: UploadFile = File(..., description="Ejercicio PDF"),
    exercise_id: str = Form(..., description="ID del ejercicio"),
    handler: UploadExerciseHandler = Depends(get_upload_exercise_handler)
) -> ResultSchema:
    try:
        content = await file.read()
        
        result = handler.execute(
            UploadExerciseDTO(
                exercise_id=exercise_id,
                file_data=BytesIO(content),
                content_type=file.content_type
            )
        )
        
        return ResultSchema(
            success=True,
            status_code="200",
            error=None,
            message="Ejercicio subido",
            data=result
        )
        
    except InvalidFileTypeError as e:
        raise HTTPException(400, str(e))
    except FileSizeExceededError as e:
        raise HTTPException(400, str(e))
    except BucketNotFoundError as e:
        raise HTTPException(500, str(e))
    except Exception as e:
        raise HTTPException(500, f"Error al subir ejercicio: {str(e)}")