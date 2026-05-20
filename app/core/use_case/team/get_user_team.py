from app.ports.driven.database.postgres.team_repository_abc import TeamRepositoryInterface
from app.ports.driving.handler_interface import HandlerInterface
from app.domain.dtos.team_dto import (
    GetTeamDetailResponseDTO,
)
from app.ports.driving.storage_bucket_interfaz import StorageBucketInterfaceABC
from app.domain.exceptions.base_exceptions import (
    TeamNotFoundException,
)


class GetUserTeamHandler(HandlerInterface):
    def __init__(
        self, team_query: TeamRepositoryInterface, storage: StorageBucketInterfaceABC
    ):
        self._team_query = team_query
        self._storage = storage

    async def execute_async(self, user_id: str) -> GetTeamDetailResponseDTO:
        if not user_id or not isinstance(user_id, str):
            raise TeamNotFoundException(user_id="invalid")

        user_team = self._team_query.get_user_team(user_id)
        if user_team and user_team.team_id:
            team_detail = self._team_query.get_team_detail_by_id(int(user_team.team_id))
            if team_detail:
                return GetTeamDetailResponseDTO(team=team_detail)

        raise TeamNotFoundException(user_id=user_id)

    def execute(self, *args, **kwargs):
        return self.execute_async(*args, **kwargs)
