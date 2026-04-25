from fastapi import APIRouter, Depends, File, UploadFile, Form, Path # type: ignore
from io import BytesIO
from app.domain.dtos.bucket_dto import (
    UploadPortraitDTO,
    UploadSponsorLogoDTO,
    UploadExerciseDTO,
    DeletePortraitDTO,
    GetPortraitDTO,
    GetSponsorLogoDTO,
    GetExerciseDTO,
)
from app.core.use_case.bucket.upload_portrait import UploadPortraitHandler
from app.core.use_case.bucket.delete_portrait import DeletePortraitHandler
from app.core.use_case.bucket.upload_sponsor_logo import UploadSponsorLogoHandler
from app.core.use_case.bucket.upload_exercise import UploadExerciseHandler
from app.core.use_case.bucket.get_portrait import GetPortraitHandler
from app.core.use_case.bucket.get_sponsor_logo import GetSponsorLogoHandler
from app.core.use_case.bucket.get_exercise import GetExerciseHandler
from app.adapters.database.dependencies import (
    get_upload_portrait_handler,
    get_delete_portrait_handler,
    get_upload_sponsor_logo_handler,
    get_upload_exercise_handler,
    get_get_portrait_handler,
    get_get_sponsor_logo_handler,
    get_get_exercise_handler,
)
from app.adapters.routing.utils.decorators import format_response
from typing import Any  

bucket_router = APIRouter(prefix="/bucket", tags=["Files"])


@bucket_router.post("/portrait")
@format_response
async def upload_portrait(
    file: UploadFile = File(..., description="Profile picture (PNG)"),
    user_id: str = Form(..., description="User ID"),
    handler: UploadPortraitHandler = Depends(get_upload_portrait_handler),
) -> Any: 
    content = await file.read()
    return await handler.execute(
        UploadPortraitDTO(
            user_id=user_id,
            file_data=BytesIO(content),
            content_type=file.content_type,
        )
    )


@bucket_router.delete("/portrait/{user_id}")
@format_response
async def delete_portrait(
    user_id: str = Path(..., description="User ID"),
    handler: DeletePortraitHandler = Depends(get_delete_portrait_handler),
) -> Any: 
    return await handler.execute(DeletePortraitDTO(user_id=user_id))


@bucket_router.get("/portrait/{user_id}")
@format_response
async def get_portrait(
    user_id: str = Path(..., description="User ID"),
    handler: GetPortraitHandler = Depends(get_get_portrait_handler),
) -> Any: 
    return await handler.execute(GetPortraitDTO(user_id=user_id))


@bucket_router.post("/sponsors/logo")
@format_response
async def upload_sponsor_logo(
    file: UploadFile = File(..., description="Sponsor logo (PNG)"),
    sponsor_id: str = Form(..., description="Sponsor ID"),
    handler: UploadSponsorLogoHandler = Depends(get_upload_sponsor_logo_handler),
) -> Any: 
    content = await file.read()
    return await handler.execute(
        UploadSponsorLogoDTO(
            sponsor_id=sponsor_id,
            file_data=BytesIO(content),
            content_type=file.content_type,
        )
    )


@bucket_router.get("/sponsors/logo/{sponsor_id}")
@format_response
async def get_sponsor_logo(
    sponsor_id: str = Path(..., description="Sponsor ID"),
    handler: GetSponsorLogoHandler = Depends(get_get_sponsor_logo_handler),
) -> Any: 
    return await handler.execute(GetSponsorLogoDTO(sponsor_id=sponsor_id))


@bucket_router.get("/exercises/{exercise_id}")
@format_response
async def get_exercise(
    exercise_id: str = Path(..., description="Exercise ID"),
    handler: GetExerciseHandler = Depends(get_get_exercise_handler),
) -> Any:
    return await handler.execute(GetExerciseDTO(exercise_id=exercise_id))


@bucket_router.post("/exercises/upload")
@format_response
async def upload_exercise(
    file: UploadFile = File(..., description="Exercise PDF"),
    exercise_id: str = Form(..., description="Exercise ID"),
    handler: UploadExerciseHandler = Depends(get_upload_exercise_handler),
) -> Any:  
    content = await file.read()
    return await handler.execute(
        UploadExerciseDTO(
            exercise_id=exercise_id,
            file_data=BytesIO(content),
            content_type=file.content_type,
        )
    )