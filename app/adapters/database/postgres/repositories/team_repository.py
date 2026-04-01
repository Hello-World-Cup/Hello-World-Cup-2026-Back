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
from app.adapters.database.postgres.models.user_model import User
from app.adapters.database.postgres.models.role_model import Role
from app.domain.enums import TeamRequestStatus, UserStatus
from typing import List


class TeamRepository(TeamQueryInterface):
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_team(self, user_id: str) -> TeamResponseDTO:
        current_edition = self.db.query(Edition)\
            .order_by(desc(Edition.start_date))\
            .first()
        
        if not current_edition:
            raise NoCurrentEditionException()
        
        team = self.db.query(Team)\
            .join(
                user_team_association,
                (Team.id == user_team_association.c.team_id) &
                (user_team_association.c.user_id == int(user_id))
            )\
            .filter(Team.edition_id == current_edition.id)\
            .first()
        
        if not team:
            raise TeamNotFoundException(user_id=user_id)
        
        stmt = select(team_request_association)\
            .where(team_request_association.c.team_id == team.id)
        requests = self.db.execute(stmt).mappings().all()
        
        deleted_members = []
        pending_members = []
        accepted_members = []
        
        for req in requests:
            user = self.db.query(User).filter(User.id == req.sender_user_id).first()
            if not user:
                continue
            
            member_dto = TeamMemberDTO(
                user_id=str(user.id),
                username=user.username,
                email=user.email,
                name=user.name,
                status=req.status.value  
            )
            
            if req.status == TeamRequestStatus.DELETED:
                deleted_members.append(member_dto)
            elif req.status == TeamRequestStatus.PENDING:
                pending_members.append(member_dto)
            elif req.status == TeamRequestStatus.ACCEPTED:
                accepted_members.append(member_dto)
        
        return TeamResponseDTO(
            team_id=str(team.id),
            team_name=team.name,
            edition_id=str(current_edition.id),
            edition_name=current_edition.name,
            created_at=team.created_at if hasattr(team, 'created_at') else None,
            updated_at=team.updated_at if hasattr(team, 'updated_at') else None,
            deleted_members=deleted_members,
            pending_members=pending_members,
            accepted_members=accepted_members
        )
    
    def get_active_users(self) -> List[UserListDTO]:
        users = self.db.query(User)\
            .join(Role, User.role_id == Role.id)\
            .filter(
                User.status == UserStatus.ACTIVE,
                not Role.is_super_user 
            ).all()
        
        return [
            UserListDTO(
                username=user.username,
                email=user.email,
                name=user.name
            )
            for user in users
        ]