from abc import ABC, abstractmethod
from typing import Any

class HandlerInterfaceABC(ABC):
    @abstractmethod
    def execute(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError("Execute method not implemented for handler.")