from app.domain.dtos.team_dto import GetTeamDetailResponseDTO
from app.domain.exceptions.base_exceptions import DomainException
from app.domain.exceptions.error_codes import TEAM_NOT_FOUND
from app.ports.driven.database.postgres.role_repository import RoleRepositoryInterface
from app.ports.driven.database.postgres.team_repository_abc import (
    TeamRepositoryInterface,
)
from app.ports.driving.handler_interface import HandlerInterface
from app.adapters.routing.utils.context import user_context


class GetTeamDetailHandler(HandlerInterface):
    def __init__(
        self,
        team_repository: TeamRepositoryInterface,
        role_repository: RoleRepositoryInterface,
    ) -> None:
        self._team_repository = team_repository
        self._role_repository = role_repository

    def execute(self, team_id: int) -> GetTeamDetailResponseDTO:
        user = user_context.get()

        if not user or not user.role_id:
            raise DomainException("Authentication required", TEAM_NOT_FOUND)

        role = self._role_repository.get_by_id(user.role_id)
        if not role:
            raise DomainException("Unauthorized", TEAM_NOT_FOUND)

        team = self._team_repository.get_team_detail_by_id(team_id)
        if not team:
            raise DomainException("Team not found", TEAM_NOT_FOUND)

        is_admin = role.is_super_user or role.internal_code == "admin"
        is_member = any(member.id == user.id for member in team.members)

        if not (is_admin or is_member):
            raise DomainException("Access denied to this team", TEAM_NOT_FOUND)

        return GetTeamDetailResponseDTO(team=team)
