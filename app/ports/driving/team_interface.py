
from abc import ABC, abstractmethod
from typing import List
from app.domain.dtos.team_dto import GetUserTeamResponseDTO, UserListDTO


class TeamQueryInterface(ABC): 
    @abstractmethod
    def get_user_team(self, user_id: str) -> GetUserTeamResponseDTO:
        raise NotImplementedError("Get user team method not implemented")
    
    @abstractmethod
    def get_active_users(self) -> List[UserListDTO]:
        raise NotImplementedError("Get active users method not implemented")
