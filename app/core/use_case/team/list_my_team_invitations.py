from app.domain.dtos.team_dto import ListMyTeamInvitationsResponseDTO
from app.ports.driven.database.postgres.team_repository_abc import (
    TeamRepositoryInterface,
)
from app.ports.driving.handler_interface import HandlerInterface


class ListMyTeamInvitationsHandler(HandlerInterface):
    def __init__(self, team_repository: TeamRepositoryInterface) -> None:
        self._team_repository = team_repository

    def execute(self, current_user_id: int) -> ListMyTeamInvitationsResponseDTO:
        invitations = self._team_repository.get_pending_team_requests_by_receiver_id(
            current_user_id
        )
        return ListMyTeamInvitationsResponseDTO(invitations=invitations)
