from datetime import datetime, timezone

from app.domain.dtos.team_dto import CreateTeamInputDTO, CreateTeamResponseDTO
from app.domain.exceptions.base_exceptions import (
    DomainException,
    RecordNotFoundException,
)
from app.domain.exceptions.error_codes import (
    TEAM_CATEGORY_NOT_FOUND,
    TEAM_EDITION_NOT_AVAILABLE,
    TEAM_LEADER_ALREADY_HAS_TEAM,
    TEAM_LEADER_NOT_CONFIRMED,
)
from app.ports.driven.database.postgres.team_repository_abc import (
    TeamRepositoryInterface,
)
from app.ports.driving.handler_interface import HandlerInterface


class CreateTeamHandler(HandlerInterface):
    def __init__(self, team_repository: TeamRepositoryInterface) -> None:
        self._team_repository = team_repository

    def execute(
        self, leader_user_id: int, data: CreateTeamInputDTO
    ) -> CreateTeamResponseDTO:
        leader = self._team_repository.get_user_by_id(leader_user_id)
        if leader is None:
            raise RecordNotFoundException("USER")

        if not leader.is_verified:
            raise DomainException(
                "The authenticated user must have a confirmed account to create a team",
                TEAM_LEADER_NOT_CONFIRMED,
            )

        if not self._team_repository.category_exists(data.category_id):
            raise DomainException("Category not found", TEAM_CATEGORY_NOT_FOUND)

        if self._team_repository.user_has_team(
            leader_user_id
        ) or self._team_repository.get_team_by_leader_id(leader_user_id):
            raise DomainException(
                "The authenticated user is already associated with a team",
                TEAM_LEADER_ALREADY_HAS_TEAM,
            )

        current_date = datetime.now(timezone.utc)
        edition_id = self._team_repository.get_latest_available_edition_id(current_date)
        if edition_id is None:
            raise DomainException(
                "There is no available edition with end_date greater than or equal to the current date",
                TEAM_EDITION_NOT_AVAILABLE,
            )

        team = self._team_repository.create_team(
            name=f"{leader.username}-team",
            edition_id=edition_id,
            category_id=data.category_id,
            leader_id=leader_user_id,
        )

        return CreateTeamResponseDTO(team=team)
