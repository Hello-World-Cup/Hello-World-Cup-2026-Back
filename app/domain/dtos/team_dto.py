from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class TeamMemberDTO(BaseModel):
    user_id: str
    username: str
    email: str
    name: str
    status: str 

class TeamResponseDTO(BaseModel):
    team_id: str
    team_name: str
    edition_id: str
    edition_name: str
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_members: List[TeamMemberDTO]
    pending_members: List[TeamMemberDTO]
    accepted_members: List[TeamMemberDTO]


class UserListDTO(BaseModel):
    username: str
    email: str
    name: str