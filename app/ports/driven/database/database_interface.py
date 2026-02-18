from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional
from pydantic import BaseModel # type: ignore

T=TypeVar("T")
T_ID=TypeVar("T_ID")
T_Create=TypeVar("T_Create", bound=BaseModel)
T_Update=TypeVar("T_Update", bound=BaseModel)
T_Read=TypeVar("T_Read", bound=BaseModel)


class UnitOfWork(ABC):
    """
    Puerto DRIVEN para transacciones/Unit of Work.
    """

    @abstractmethod
    def begin(self) -> None:
        """Inicia una transacción."""
        pass

    @abstractmethod
    def commit(self) -> None:
        """Confirma la transacción actual."""
        pass

    @abstractmethod
    def rollback(self) -> None:
        """Deshace la transacción actual."""
        pass

    @abstractmethod
    def __enter__(self):
        """Context manager para transacciones."""
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager para transacciones."""
        pass


class CRUDRepository(ABC, Generic[T_Create, T_Update, T_Read, T_ID]):
    @abstractmethod
    def create(self, data: T_Create) -> T_Read:
        raise NotImplementedError("Create method not implemented!")

    @abstractmethod
    def read(self, id: T_ID) -> Optional[T_Read]:
        raise NotImplementedError("Read method not implemented!")
    @abstractmethod
    def update(self, id: T_ID, data: T_Update) -> Optional[T_Read]:
        raise NotImplementedError("Update method not implemented!")

    @abstractmethod
    def delete(self, id: T_ID) -> None:
        raise NotImplementedError("Delete method not implemented!")
