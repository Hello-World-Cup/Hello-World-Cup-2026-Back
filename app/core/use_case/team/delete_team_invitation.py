from app.domain.dtos.team_dto import DeleteTeamInvitationResponseDTO
from app.domain.enums import TeamRequestStatus
from app.domain.exceptions.base_exceptions import DomainException
from app.domain.exceptions.error_codes import (
    TEAM_REQUEST_FORBIDDEN,
    TEAM_REQUEST_INVALID_STATUS,
    TEAM_REQUEST_NOT_FOUND,
)
from app.ports.driven.database.postgres.team_repository_abc import (
    TeamRepositoryInterface,
)
from app.ports.driving.handler_interface import HandlerInterface


class DeleteTeamInvitationHandler(HandlerInterface):
    def __init__(self, team_repository: TeamRepositoryInterface) -> None:
        self._team_repository = team_repository

    def execute(
        self,
        current_user_id: int,
        team_request_id: int,
    ) -> DeleteTeamInvitationResponseDTO:
        team_request = self._team_repository.get_team_request_by_id(team_request_id)
        if team_request is None:
            raise DomainException("Invitation not found", TEAM_REQUEST_NOT_FOUND)

        if current_user_id not in {
            team_request.sender_user_id,
            team_request.receiver_user_id,
        }:
            raise DomainException(
                "The authenticated user cannot delete this invitation",
                TEAM_REQUEST_FORBIDDEN,
            )

        if team_request.status != TeamRequestStatus.PENDING:
            raise DomainException(
                "Only pending invitations can be deleted",
                TEAM_REQUEST_INVALID_STATUS,
            )

        deleted_request = self._team_repository.update_team_request_status(
            team_request_id=team_request_id,
            status=TeamRequestStatus.DELETED,
        )

        return DeleteTeamInvitationResponseDTO(
            team_request_id=deleted_request.id,
            status=deleted_request.status,
        )
