from app.domain.dtos.team_dto import DeleteTeamResponseDTO
from app.domain.exceptions.base_exceptions import DomainException
from app.domain.exceptions.error_codes import TEAM_FORBIDDEN, TEAM_NOT_FOUND
from app.ports.driven.database.postgres.team_repository_abc import (
    TeamRepositoryInterface,
)
from app.ports.driving.handler_interface import HandlerInterface


class DeleteTeamHandler(HandlerInterface):
    def __init__(self, team_repository: TeamRepositoryInterface) -> None:
        self._team_repository = team_repository

    def execute(self, current_user_id: int, team_id: int) -> DeleteTeamResponseDTO:
        team = self._team_repository.get_team_by_id(team_id)
        if team is None:
            raise DomainException("Team not found", TEAM_NOT_FOUND)

        if team.assigned_evaluator_id != current_user_id:
            raise DomainException(
                "The authenticated user cannot delete this team",
                TEAM_FORBIDDEN,
            )

        deleted_team_requests, deleted_user_team_associations = (
            self._team_repository.delete_team_with_associations(team_id)
        )

        return DeleteTeamResponseDTO(
            team_id=team_id,
            deleted_team_requests=deleted_team_requests,
            deleted_user_team_associations=deleted_user_team_associations,
        )
