from sqlalchemy.orm import Session
from sqlalchemy import desc, select
from app.ports.driving.team_interface import TeamQueryInterface
from app.domain.dtos.team_dto import TeamResponseDTO, TeamMemberDTO, UserListDTO
from app.domain.exceptions.base_exceptions import (
    TeamNotFoundException,
    NoCurrentEditionException,
)
from app.adapters.database.postgres.models.team_model import (
    Team
)
from app.adapters.database.postgres.models.user_model import (
    User,
    user_team_association,
    team_request_association
)
from app.adapters.database.postgres.models.edition_model import Edition
from app.adapters.database.postgres.models.role_model import Role
from app.domain.enums import TeamRequestStatus, UserStatus
from typing import List


class TeamRepository(TeamQueryInterface):
    def __init__(self, db: Session) -> None:
        self.db = db
    
    def get_user_team(self, user_id: str) -> TeamResponseDTO:
        current_edition = self.db.query(Edition)\
            .order_by(desc(Edition.start_date))\
            .first()
        
        if not current_edition:
            raise NoCurrentEditionException()
        
        team = self.db.query(Team)\
            .join(user_team_association)\
            .filter(
                user_team_association.c.user_id == int(user_id),
                Team.edition_id == current_edition.id
            )\
            .first()
        
        if not team:
            raise TeamNotFoundException(user_id=user_id)
        
        stmt = (
            select(
                User.id, 
                User.username, 
                User.email, 
                User.name, 
                team_request_association.c.status
            )
            .join(User, User.id == team_request_association.c.sender_user_id)
            .where(team_request_association.c.team_id == team.id)
        )
        
        members_data = self.db.execute(stmt).all()
        
        categorized = {
            TeamRequestStatus.DELETED: [],
            TeamRequestStatus.PENDING: [],
            TeamRequestStatus.ACCEPTED: []
        }
        
        for row in members_data:
            member_dto = TeamMemberDTO(
                user_id=str(row.id),
                username=row.username,
                email=row.email,
                name=row.name,
                status=TeamRequestStatus(row.status).name
            )
            if row.status in categorized:
                categorized[row.status].append(member_dto)
        
        return TeamResponseDTO(
            team_id=str(team.id),
            team_name=team.name,
            edition_id=str(current_edition.id),
            edition_name=current_edition.name,
            created_at=getattr(team, 'created_at', None),
            updated_at=getattr(team, 'updated_at', None),
            deleted_members=categorized[TeamRequestStatus.DENIED],
            pending_members=categorized[TeamRequestStatus.PENDING],
            accepted_members=categorized[TeamRequestStatus.ACCEPTED]
        )
    
    def get_active_users(self) -> List[UserListDTO]:
        users = self.db.query(User)\
            .join(Role, User.role_id == Role.id)\
            .filter(
                User.status == UserStatus.ACTIVE,
                Role.is_super_user == False 
            ).all()
        
        return [
            UserListDTO(
                username=user.username,
                email=user.email,
                name=user.name
            )
            for user in users
        ]