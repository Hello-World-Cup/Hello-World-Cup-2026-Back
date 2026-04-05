from app.domain.dtos.team_dto import (
    SendTeamInvitationsInputDTO,
    SendTeamInvitationsResponseDTO,
)
from app.domain.exceptions.base_exceptions import (
    DomainException,
    RecordNotFoundException,
)
from app.domain.exceptions.error_codes import (
    TEAM_LEADER_TEAM_NOT_FOUND,
    TEAM_REQUEST_EMPTY_USERNAMES,
)
from app.ports.driven.database.postgres.team_repository_abc import (
    TeamRepositoryInterface,
)
from app.ports.driving.handler_interface import HandlerInterface


class SendTeamInvitationsHandler(HandlerInterface):
    def __init__(self, team_repository: TeamRepositoryInterface) -> None:
        self._team_repository = team_repository

    def execute(
        self,
        sender_user_id: int,
        data: SendTeamInvitationsInputDTO,
    ) -> SendTeamInvitationsResponseDTO:
        normalized_usernames: list[str] = []
        duplicated_usernames: list[str] = []
        seen_usernames: set[str] = set()

        for username in data.usernames:
            normalized_username = username.strip().lower()
            if not normalized_username:
                continue

            if normalized_username in seen_usernames:
                duplicated_usernames.append(normalized_username)
                continue

            seen_usernames.add(normalized_username)
            normalized_usernames.append(normalized_username)

        if not normalized_usernames:
            raise DomainException(
                "The usernames list must contain at least one valid username",
                TEAM_REQUEST_EMPTY_USERNAMES,
            )

        team = self._team_repository.get_team_by_leader_id(sender_user_id)
        if team is None:
            raise DomainException(
                "The authenticated user does not lead any team",
                TEAM_LEADER_TEAM_NOT_FOUND,
            )

        users = self._team_repository.get_users_by_usernames(normalized_usernames)
        users_by_username = {
            (user.username or "").strip().lower(): user for user in users
        }

        not_found_usernames: list[str] = []
        not_confirmed_usernames: list[str] = []
        usernames_with_team: list[str] = []
        self_invitation_usernames: list[str] = []

        valid_user_ids: list[int] = []
        valid_usernames_by_id: dict[int, str] = {}

        for username in normalized_usernames:
            user = users_by_username.get(username)
            if user is None:
                not_found_usernames.append(username)
                continue

            if user.id == sender_user_id:
                self_invitation_usernames.append(username)
                continue

            if not user.is_verified:
                not_confirmed_usernames.append(username)
                continue

            if user.id is None:
                raise RecordNotFoundException("USER")

            if self._team_repository.user_has_team(user.id):
                usernames_with_team.append(username)
                continue

            valid_user_ids.append(user.id)
            valid_usernames_by_id[user.id] = username

        already_invited_ids = self._team_repository.get_pending_request_receiver_ids(
            team.id,
            valid_user_ids,
        )

        already_invited_usernames = [
            valid_usernames_by_id[user_id]
            for user_id in valid_user_ids
            if user_id in already_invited_ids
        ]

        receiver_user_ids_to_invite = [
            user_id for user_id in valid_user_ids if user_id not in already_invited_ids
        ]

        created_requests = self._team_repository.create_team_requests(
            team_id=team.id,
            sender_user_id=sender_user_id,
            receiver_user_ids=receiver_user_ids_to_invite,
        )

        return SendTeamInvitationsResponseDTO(
            message="Invitations processed successfully",
            team_id=team.id,
            created_requests=created_requests,
            not_found_usernames=not_found_usernames,
            not_confirmed_usernames=not_confirmed_usernames,
            usernames_with_team=usernames_with_team,
            already_invited_usernames=already_invited_usernames,
            duplicated_usernames=duplicated_usernames,
            self_invitation_usernames=self_invitation_usernames,
        )
