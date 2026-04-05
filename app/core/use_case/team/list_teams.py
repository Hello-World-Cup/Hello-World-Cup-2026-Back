from app.domain.dtos.team_dto import ListTeamsResponseDTO
from app.ports.driven.database.postgres.team_repository_abc import (
    TeamRepositoryInterface,
)
from app.ports.driving.handler_interface import HandlerInterface


class ListTeamsHandler(HandlerInterface):
    def __init__(self, team_repository: TeamRepositoryInterface) -> None:
        self._team_repository = team_repository

    def execute(self) -> ListTeamsResponseDTO:
        teams = self._team_repository.list_teams()
        return ListTeamsResponseDTO(teams=teams)
