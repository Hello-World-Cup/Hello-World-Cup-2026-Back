from app.domain.dtos.team_dto import GetTeamDetailResponseDTO
from app.domain.exceptions.base_exceptions import DomainException
from app.domain.exceptions.error_codes import TEAM_NOT_FOUND
from app.ports.driven.database.postgres.team_repository_abc import (
    TeamRepositoryInterface,
)
from app.ports.driving.handler_interface import HandlerInterface


class GetTeamDetailHandler(HandlerInterface):
    def __init__(self, team_repository: TeamRepositoryInterface) -> None:
        self._team_repository = team_repository

    def execute(self, team_id: int) -> GetTeamDetailResponseDTO:
        team_detail = self._team_repository.get_team_detail_by_id(team_id)
        if team_detail is None:
            raise DomainException("Team not found", TEAM_NOT_FOUND)

        return GetTeamDetailResponseDTO(team=team_detail)
