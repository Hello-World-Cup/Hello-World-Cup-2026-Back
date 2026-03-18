from datetime import datetime, timezone
import hashlib

from app.domain.dtos.user_dto import SignOutInputDTO, SignOutResponseDTO
from app.ports.driving.handler_interface import HandlerInterface
from app.ports.driven.database.postgres.refresh_token_repository_abc import RefreshTokenRepositoryInterface


class SignOutHandler(HandlerInterface):
    def __init__(self, refresh_repo: RefreshTokenRepositoryInterface) -> None:
        self._refresh_repo = refresh_repo

    def execute(self, data: SignOutInputDTO) -> SignOutResponseDTO:
        now = datetime.now(timezone.utc)
        token_hash = hashlib.sha256(data.refresh_token.encode("utf-8")).hexdigest()

        stored = self._refresh_repo.get_by_hash(token_hash)
        if not stored:
            # do not reveal info, just respond OK
            return SignOutResponseDTO()

        if stored.revoked_at is None:
            self._refresh_repo.revoke(stored.id, revoked_at=now)

        return SignOutResponseDTO()