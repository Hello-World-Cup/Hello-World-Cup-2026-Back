from typing import Optional
from sqlalchemy.orm import Session

from app.ports.driven.database.postgres.test_repository_abc import TestRepositoryABC
from app.domain.dtos.test_dto import TestDTO
from app.adapters.database.postgres.models import Test
from app.domain.exceptions.base_exceptions import RecordNotFoundException 

class TestRepository(TestRepositoryABC):
    def __init__(self, db: Session) -> None:
        self.db = db
        
    def create(self, data: TestDTO) -> TestDTO:
        create_data = data.model_dump(exclude_unset=True, exclude={"id"})
        test_orm = Test(**create_data)
        
        self.db.add(test_orm)
        self.db.commit()
        self.db.refresh(test_orm)

        return TestDTO.from_orm(test_orm)

    def read(self, id: int) -> Optional[TestDTO]:
        query_result = self.db.query(Test).filter_by(id=id).first()
        if not query_result:
            raise RecordNotFoundException("TEST")
        return TestDTO.from_orm(query_result)

    def update(self, id: int, data: TestDTO) -> Optional[TestDTO]:
        update_data = data.model_dump(exclude_unset=True)
        update_data.pop("id", None)
    
        query_result = self.db.query(Test).filter_by(id=id).first()
        
        if query_result:
            for key, value in update_data.items():
                setattr(query_result, key, value)
            
            self.db.commit()
            self.db.refresh(query_result)
            return TestDTO.from_orm(query_result)
        
        raise RecordNotFoundException("TEST")

    def delete(self, id: int) -> None:
        query_result = self.db.query(Test).filter_by(id=id).first()
        if not query_result:
            raise RecordNotFoundException("TEST")
        self.db.delete(query_result)
        self.db.commit()
