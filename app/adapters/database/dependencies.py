from sqlalchemy.orm import Session
from app.core.use_case.test.delete_test import DeleteTestByIdHandler
from app.core.use_case.test.get_test import GetTestByIdHandler
from fastapi import Depends # type: ignore

from app.adapters.database.postgres.repositories.test_repository import TestRepository
from app.adapters.database.postgres.connection import get_db


# Repositories

def get_test_repository(db: Session) -> TestRepository:
    return TestRepository(db)


# Use cases

def get_test_by_id_handler(db: Session = Depends(get_db)) -> GetTestByIdHandler:
    return GetTestByIdHandler(get_test_repository(db))

def delete_test_by_id_handler(db: Session = Depends(get_db)) -> DeleteTestByIdHandler:
    return DeleteTestByIdHandler(get_test_repository(db))

