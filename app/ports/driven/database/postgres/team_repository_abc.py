from abc import ABC, abstractmethod
from datetime import datetime

from app.domain.dtos.team_dto import (
    TeamDetailDTO,
    TeamInvitationSummaryDTO,
    TeamListItemDTO,
    TeamRequestDTO,
    TeamResponseDTO,
)
from app.domain.dtos.user_dto import UserDTO
from app.domain.enums import TeamRequestStatus


class TeamRepositoryInterface(ABC):
    @abstractmethod
    def category_exists(self, category_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_latest_available_edition_id(self, current_date: datetime) -> int | None:
        raise NotImplementedError

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> UserDTO | None:
        raise NotImplementedError

    @abstractmethod
    def get_users_by_usernames(self, usernames: list[str]) -> list[UserDTO]:
        raise NotImplementedError

    @abstractmethod
    def user_has_team(self, user_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_team_by_leader_id(self, leader_id: int) -> TeamResponseDTO | None:
        raise NotImplementedError

    @abstractmethod
    def get_team_by_id(self, team_id: int) -> TeamResponseDTO | None:
        raise NotImplementedError

    @abstractmethod
    def list_teams(self) -> list[TeamListItemDTO]:
        raise NotImplementedError

    @abstractmethod
    def get_team_detail_by_id(self, team_id: int) -> TeamDetailDTO | None:
        raise NotImplementedError

    @abstractmethod
    def create_team(
        self,
        name: str,
        edition_id: int,
        category_id: int,
        leader_id: int,
    ) -> TeamResponseDTO:
        raise NotImplementedError

    @abstractmethod
    def get_pending_request_receiver_ids(
        self,
        team_id: int,
        receiver_user_ids: list[int],
    ) -> set[int]:
        raise NotImplementedError

    @abstractmethod
    def create_team_requests(
        self,
        team_id: int,
        sender_user_id: int,
        receiver_user_ids: list[int],
    ) -> list[TeamRequestDTO]:
        raise NotImplementedError

    @abstractmethod
    def get_team_request_by_id(self, team_request_id: int) -> TeamRequestDTO | None:
        raise NotImplementedError

    @abstractmethod
    def get_pending_team_requests_by_receiver_id(
        self, receiver_user_id: int
    ) -> list[TeamInvitationSummaryDTO]:
        raise NotImplementedError

    @abstractmethod
    def update_team_request_status(
        self,
        team_request_id: int,
        status: TeamRequestStatus,
    ) -> TeamRequestDTO:
        raise NotImplementedError

    @abstractmethod
    def accept_team_request_and_assign_user(
        self,
        team_request_id: int,
    ) -> tuple[TeamRequestDTO, int]:
        raise NotImplementedError

    @abstractmethod
    def delete_team_with_associations(self, team_id: int) -> tuple[int, int]:
        raise NotImplementedError
