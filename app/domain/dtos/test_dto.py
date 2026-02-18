from pydantic import BaseModel, Field # type: ignore


class TestDTO(BaseModel):
    id: int | None=Field(default=None)
    message: str | None=Field(default=None)

    @classmethod
    def from_orm(cls, orm_obj: object) -> "TestDTO":
        return cls(
            id=getattr(orm_obj, "id", None), message=getattr(orm_obj, "message", None)
        )