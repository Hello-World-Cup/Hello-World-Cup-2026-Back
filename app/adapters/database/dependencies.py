from sqlalchemy.orm import Session
from app.core.use_case.test.delete_test import DeleteTestByIdHandler
from app.core.use_case.test.get_test import GetTestByIdHandler
from fastapi import Depends # type: ignore

from app.adapters.database.postgres.repositories.test_repository import TestRepository
from app.adapters.database.postgres.connection import get_db


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

