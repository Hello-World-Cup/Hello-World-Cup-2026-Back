from sqlalchemy import TypeDecorator
from sqlalchemy.dialects.postgresql import JSONB # type: ignore
from pydantic import BaseModel # type: ignore
from typing import Type


class PydanticJSONB(TypeDecorator):
    impl=JSONB
    cache_ok=True

    def __init__(self, model_class: Type[BaseModel], *args, **kwargs):
        self.model_class=model_class
        super().__init__(*args, **kwargs)

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if isinstance(value, self.model_class):
            return value.model_dump()
        if isinstance(value, dict):
            return self.model_class(**value).model_dump()
        raise ValueError(f"Expected {self.model_class.__name__}, got {type(value)}")

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        if isinstance(value, dict):
            return self.model_class(**value)
        return value
