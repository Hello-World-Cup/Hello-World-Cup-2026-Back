from abc import ABC, abstractmethod
from typing import Optional, Any
from datetime import datetime


class RefreshTokenRepositoryInterface(ABC):
    @abstractmethod
    def create(
        self,
        user_id: int,
        token_hash: str,
        issued_at: datetime,
        expires_at: datetime,
        user_agent: str | None = None,
        ip_address: str | None = None,
    ) -> Any:
        raise NotImplementedError

    @abstractmethod
    def get_by_hash(self, token_hash: str) -> Optional[Any]:
        raise NotImplementedError

    @abstractmethod
    def revoke(self, token_id: int, revoked_at: datetime, replaced_by_token_id: int | None = None) -> None:
        raise NotImplementedError

    @abstractmethod
    def revoke_all_for_user(self, user_id: int, revoked_at: datetime) -> None:
        raise NotImplementedError