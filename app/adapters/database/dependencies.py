from sqlalchemy.orm import Session
from app.core.use_case.test.delete_test import DeleteTestByIdHandler
from app.core.use_case.test.get_test import GetTestByIdHandler
from fastapi import Depends # type: ignore

from app.adapters.database.postgres.repositories.test_repository import TestRepository
from app.adapters.database.postgres.connection import get_db
from app.adapters.supabase.supabase_connection import supabase_client
from app.adapters.supabase.supabase_storage import StorageBucketSupabase
from app.ports.driving.storage_bucket_interfaz import StorageBucketInterfaceABC

from app.core.use_case.bucket.upload_portrait import UploadPortraitHandler
from app.core.use_case.bucket.delete_portrait import DeletePortraitHandler
from app.core.use_case.bucket.upload_sponsor_logo import UploadSponsorLogoHandler
from app.core.use_case.bucket.upload_exercise import UploadExerciseHandler



# Authorization
# TODO: Una vez que el middleware de autenticación haga su trabajo e inyecte al usuario al ContextVar, se obtendrá acá y se validará que su rol concuerde con el required_rol
def get_authorized_user(required_role: str) -> None:
    pass

# Repositories

def get_test_repository(db: Session) -> TestRepository:
    return TestRepository(db)


# Use cases

def get_test_by_id_handler(db: Session=Depends(get_db)) -> GetTestByIdHandler:
    return GetTestByIdHandler(get_test_repository(db))

def delete_test_by_id_handler(db: Session=Depends(get_db)) -> DeleteTestByIdHandler:
    return DeleteTestByIdHandler(get_test_repository(db))

def get_supabase_client() -> StorageBucketInterfaceABC:
    return StorageBucketSupabase(supabase_client())

def get_upload_portrait_handler(
    storage: StorageBucketInterfaceABC = Depends(get_supabase_client)
) -> UploadPortraitHandler:
    return UploadPortraitHandler(storage)


def get_delete_portrait_handler(
    storage: StorageBucketInterfaceABC = Depends(get_supabase_client)
) -> DeletePortraitHandler:
    return DeletePortraitHandler(storage)


def get_upload_sponsor_logo_handler(
    storage: StorageBucketInterfaceABC = Depends(get_supabase_client)
) -> UploadSponsorLogoHandler:
    return UploadSponsorLogoHandler(storage)


def get_upload_exercise_handler(
    storage: StorageBucketInterfaceABC = Depends(get_supabase_client)
) -> UploadExerciseHandler:
    return UploadExerciseHandler(storage)