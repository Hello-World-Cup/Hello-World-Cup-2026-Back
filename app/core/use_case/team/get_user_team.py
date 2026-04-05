from app.ports.driving.team_interface import TeamQueryInterface
from app.ports.driving.handler_interface import HandlerInterface
from app.domain.dtos.team_dto import GetUserTeamResponseDTO
from app.domain.exceptions.base_exceptions import (
    TeamNotFoundException,
)


class GetUserTeamHandler(HandlerInterface):
    def __init__(self, team_query: TeamQueryInterface):
        self._team_query = team_query
    
    def execute(self, user_id: str) -> GetUserTeamResponseDTO:

        if not user_id or not isinstance(user_id, str):
            raise TeamNotFoundException(user_id="invalid")
        
        return self._team_query.get_user_team(user_id)
