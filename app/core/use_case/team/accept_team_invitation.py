from app.domain.dtos.team_dto import AcceptTeamInvitationResponseDTO
from app.domain.enums import TeamRequestStatus
from app.domain.exceptions.base_exceptions import DomainException
from app.domain.exceptions.error_codes import (
    TEAM_NOT_FOUND,
    TEAM_REQUEST_FORBIDDEN,
    TEAM_REQUEST_INVALID_STATUS,
    TEAM_REQUEST_NOT_FOUND,
    TEAM_USER_ALREADY_HAS_TEAM,
)
from app.ports.driven.database.postgres.team_repository_abc import (
    TeamRepositoryInterface,
)
from app.ports.driving.handler_interface import HandlerInterface


class AcceptTeamInvitationHandler(HandlerInterface):
    def __init__(self, team_repository: TeamRepositoryInterface) -> None:
        self._team_repository = team_repository

    def execute(
        self,
        current_user_id: int,
        team_request_id: int,
    ) -> AcceptTeamInvitationResponseDTO:
        team_request = self._team_repository.get_team_request_by_id(team_request_id)
        if team_request is None:
            raise DomainException("Invitation not found", TEAM_REQUEST_NOT_FOUND)

        if team_request.receiver_user_id != current_user_id:
            raise DomainException(
                "The authenticated user cannot accept this invitation",
                TEAM_REQUEST_FORBIDDEN,
            )

        if team_request.status != TeamRequestStatus.PENDING:
            raise DomainException(
                "Only pending invitations can be accepted",
                TEAM_REQUEST_INVALID_STATUS,
            )

        if self._team_repository.user_has_team(current_user_id):
            raise DomainException(
                "The authenticated user already has an assigned team",
                TEAM_USER_ALREADY_HAS_TEAM,
            )

        accepted_request, deleted_other_pending_invitations = (
            self._team_repository.accept_team_request_and_assign_user(team_request_id)
        )

        team = self._team_repository.get_team_by_id(accepted_request.team_id)
        if team is None:
            raise DomainException("Team not found", TEAM_NOT_FOUND)

        return AcceptTeamInvitationResponseDTO(
            team_request_id=accepted_request.id,
            team=team,
            status=accepted_request.status,
            deleted_other_pending_invitations=deleted_other_pending_invitations,
        )
