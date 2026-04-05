from datetime import datetime

from sqlalchemy import delete, func, select, update
from sqlalchemy.orm import Session, aliased

from app.adapters.database.postgres.models.category_model import Category
from app.adapters.database.postgres.models.edition_model import Edition
from app.adapters.database.postgres.models.team_model import Team
from app.adapters.database.postgres.models.user_model import (
    User,
    team_request_association,
    user_team_association,
)
from app.domain.dtos.team_dto import (
    GetUserTeamResponseDTO,
    TeamDetailDTO,
    TeamInvitationSummaryDTO,
    TeamListItemDTO,
    TeamRequestDTO,
    TeamResponseDTO,
)
from app.domain.dtos.user_dto import UserDTO, UserResponseDTO
from app.domain.enums import TeamRequestStatus
from app.domain.exceptions.base_exceptions import RecordNotFoundException
from app.ports.driven.database.postgres.team_repository_abc import (
    TeamRepositoryInterface,
)

from sqlalchemy import desc, select
from app.adapters.database.postgres.models.role_model import Role
from app.domain.enums import TeamRequestStatus, UserStatus
from app.domain.dtos.team_dto import TeamMemberDTO, TeamResponseDTO, UserListDTO
from app.domain.exceptions.base_exceptions import (
    NoCurrentEditionException,
    TeamNotFoundException,
)
from typing import List


class TeamRepository(TeamRepositoryInterface):
    def __init__(self, db: Session) -> None:
        self.db = db

    def category_exists(self, category_id: int) -> bool:
        return (
            self.db.query(Category).filter(Category.id == category_id).first()
            is not None
        )

    def get_latest_available_edition_id(self, current_date: datetime) -> int | None:
        edition = (
            self.db.query(Edition)
            .filter(Edition.end_date >= current_date)
            .order_by(Edition.id.desc())
            .first()
        )
        return edition.id if edition else None

    def get_user_by_id(self, user_id: int) -> UserDTO | None:
        user = self.db.query(User).filter(User.id == user_id).first()
        return UserDTO.from_orm(user) if user else None

    def get_users_by_usernames(self, usernames: list[str]) -> list[UserDTO]:
        if not usernames:
            return []

        normalized_usernames = [username.strip().lower() for username in usernames]
        users = (
            self.db.query(User)
            .filter(func.lower(User.username).in_(normalized_usernames))
            .all()
        )
        return [UserDTO.from_orm(user) for user in users]

    def user_has_team(self, user_id: int) -> bool:
        result = self.db.execute(
            select(user_team_association.c.user_id).where(
                user_team_association.c.user_id == user_id
            )
        ).first()
        return result is not None

    def get_team_by_leader_id(self, leader_id: int) -> TeamResponseDTO | None:
        team = (
            self.db.query(Team)
            .filter(Team.assigned_evaluator_id == leader_id)
            .order_by(Team.id.desc())
            .first()
        )
        return TeamResponseDTO.from_orm(team) if team else None

    def get_team_by_id(self, team_id: int) -> TeamResponseDTO | None:
        team = self.db.query(Team).filter(Team.id == team_id).first()
        return TeamResponseDTO.from_orm(team) if team else None

    def list_teams(self) -> list[TeamListItemDTO]:
        leader_user = aliased(User)

        rows = self.db.execute(
            select(
                Team,
                leader_user,
                func.count(user_team_association.c.user_id).label("members_count"),
            )
            .select_from(Team)
            .outerjoin(
                leader_user,
                leader_user.id == Team.assigned_evaluator_id,
            )
            .outerjoin(
                user_team_association,
                user_team_association.c.team_id == Team.id,
            )
            .group_by(Team.id, leader_user.id)
            .order_by(Team.id.desc())
        ).all()

        return [
            TeamListItemDTO(
                team=TeamResponseDTO.from_orm(row[0]),
                leader=UserResponseDTO.from_orm(row[1]) if row[1] else None,
                members_count=int(row[2] or 0),
            )
            for row in rows
        ]

    def get_user_team(self, user_id: str) -> GetUserTeamResponseDTO:
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
        
        categorized = {
            TeamRequestStatus.DELETED: [],
            TeamRequestStatus.PENDING: [],
            TeamRequestStatus.ACCEPTED: []
        }

        accepted_members_stmt = (
            select(
                User.id,
                User.username,
                User.email,
                User.name,
            )
            .join(user_team_association, user_team_association.c.user_id == User.id)
            .where(user_team_association.c.team_id == team.id)
            .order_by(User.id.asc())
        )

        accepted_members_data = self.db.execute(accepted_members_stmt).all()

        for row in accepted_members_data:
            categorized[TeamRequestStatus.ACCEPTED].append(
                TeamMemberDTO(
                    user_id=str(row.id),
                    username=row.username,
                    email=row.email,
                    name=row.name,
                    status=TeamRequestStatus.ACCEPTED.name,
                )
            )

        invited_members_stmt = (
            select(
                User.id,
                User.username,
                User.email,
                User.name,
                team_request_association.c.status,
            )
            .select_from(team_request_association)
            .join(User, User.id == team_request_association.c.receiver_user_id)
            .where(
                team_request_association.c.team_id == team.id,
                team_request_association.c.status.in_(
                    [TeamRequestStatus.PENDING, TeamRequestStatus.DELETED]
                ),
            )
            .order_by(team_request_association.c.id.asc())
        )

        invited_members_data = self.db.execute(invited_members_stmt).all()

        for row in invited_members_data:
            categorized[row.status].append(
                TeamMemberDTO(
                    user_id=str(row.id),
                    username=row.username,
                    email=row.email,
                    name=row.name,
                    status=TeamRequestStatus(row.status).name,
                )
            )
        
        return GetUserTeamResponseDTO(
            team_id=str(team.id),
            team_name=team.name,
            edition_id=str(current_edition.id),
            edition_name=current_edition.name,
            created_at=getattr(team, 'created_at', None),
            updated_at=getattr(team, 'updated_at', None),
            deleted_members=categorized[TeamRequestStatus.DELETED],
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

    def get_team_detail_by_id(self, team_id: int) -> TeamDetailDTO | None:
        team_orm = self.db.query(Team).filter(Team.id == team_id).first()
        if team_orm is None:
            return None

        leader_orm = None
        if team_orm.assigned_evaluator_id is not None:
            leader_orm = (
                self.db.query(User)
                .filter(User.id == team_orm.assigned_evaluator_id)
                .first()
            )

        member_orms = (
            self.db.query(User)
            .join(
                user_team_association,
                user_team_association.c.user_id == User.id,
            )
            .filter(user_team_association.c.team_id == team_id)
            .order_by(User.id.asc())
            .all()
        )

        members = [UserResponseDTO.from_orm(member) for member in member_orms]

        return TeamDetailDTO(
            team=TeamResponseDTO.from_orm(team_orm),
            leader=UserResponseDTO.from_orm(leader_orm) if leader_orm else None,
            members=members,
            members_count=len(members),
        )

    def create_team(
        self,
        name: str,
        edition_id: int,
        category_id: int,
        leader_id: int,
    ) -> TeamResponseDTO:
        team = Team(
            name=name,
            logo=None,
            score=None,
            standing_position=None,
            cloud_repo_link=None,
            edition_id=edition_id,
            category_id=category_id,
            evaluation_id=None,
            assigned_evaluator_id=leader_id,
        )

        try:
            self.db.add(team)
            self.db.flush()

            self.db.execute(
                user_team_association.insert().values(
                    user_id=leader_id,
                    team_id=team.id,
                )
            )

            self.db.commit()
            self.db.refresh(team)
            return TeamResponseDTO.from_orm(team)
        except Exception:
            self.db.rollback()
            raise

    def get_pending_request_receiver_ids(
        self,
        team_id: int,
        receiver_user_ids: list[int],
    ) -> set[int]:
        if not receiver_user_ids:
            return set()

        rows = self.db.execute(
            select(team_request_association.c.receiver_user_id).where(
                team_request_association.c.team_id == team_id,
                team_request_association.c.receiver_user_id.in_(receiver_user_ids),
                team_request_association.c.status == TeamRequestStatus.PENDING,
            )
        ).all()

        return {int(row[0]) for row in rows}

    def create_team_requests(
        self,
        team_id: int,
        sender_user_id: int,
        receiver_user_ids: list[int],
    ) -> list[TeamRequestDTO]:
        if not receiver_user_ids:
            return []

        try:
            rows = []
            for receiver_user_id in receiver_user_ids:
                row = self.db.execute(
                    team_request_association.insert()
                    .values(
                        team_id=team_id,
                        sender_user_id=sender_user_id,
                        receiver_user_id=receiver_user_id,
                        status=TeamRequestStatus.PENDING,
                    )
                    .returning(
                        team_request_association.c.id,
                        team_request_association.c.team_id,
                        team_request_association.c.sender_user_id,
                        team_request_association.c.receiver_user_id,
                        team_request_association.c.status,
                    )
                ).first()
                if row is None:
                    raise RecordNotFoundException("TEAM_REQUEST")
                rows.append(row)

            self.db.commit()
        except Exception:
            self.db.rollback()
            raise

        return [
            TeamRequestDTO(
                id=row.id,
                team_id=row.team_id,
                sender_user_id=row.sender_user_id,
                receiver_user_id=row.receiver_user_id,
                status=row.status,
            )
            for row in rows
        ]

    def get_team_request_by_id(self, team_request_id: int) -> TeamRequestDTO | None:
        row = self.db.execute(
            select(
                team_request_association.c.id,
                team_request_association.c.team_id,
                team_request_association.c.sender_user_id,
                team_request_association.c.receiver_user_id,
                team_request_association.c.status,
            ).where(team_request_association.c.id == team_request_id)
        ).first()

        if row is None:
            return None

        return TeamRequestDTO(
            id=row.id,
            team_id=row.team_id,
            sender_user_id=row.sender_user_id,
            receiver_user_id=row.receiver_user_id,
            status=row.status,
        )

    def get_pending_team_requests_by_receiver_id(
        self, receiver_user_id: int
    ) -> list[TeamInvitationSummaryDTO]:
        sender_user = aliased(User)

        rows = self.db.execute(
            select(
                team_request_association.c.id.label("team_request_id"),
                team_request_association.c.team_id,
                Team.name.label("team_name"),
                team_request_association.c.sender_user_id,
                sender_user.username.label("sender_username"),
                team_request_association.c.status,
            )
            .select_from(team_request_association)
            .join(Team, Team.id == team_request_association.c.team_id)
            .join(
                sender_user,
                sender_user.id == team_request_association.c.sender_user_id,
            )
            .where(
                team_request_association.c.receiver_user_id == receiver_user_id,
                team_request_association.c.status == TeamRequestStatus.PENDING,
            )
            .order_by(team_request_association.c.id.desc())
        ).all()

        return [
            TeamInvitationSummaryDTO(
                team_request_id=row.team_request_id,
                team_id=row.team_id,
                team_name=row.team_name,
                sender_user_id=row.sender_user_id,
                sender_username=row.sender_username,
                status=row.status,
            )
            for row in rows
        ]

    def update_team_request_status(
        self,
        team_request_id: int,
        status: TeamRequestStatus,
    ) -> TeamRequestDTO:
        try:
            row = self.db.execute(
                update(team_request_association)
                .where(team_request_association.c.id == team_request_id)
                .values(status=status)
                .returning(
                    team_request_association.c.id,
                    team_request_association.c.team_id,
                    team_request_association.c.sender_user_id,
                    team_request_association.c.receiver_user_id,
                    team_request_association.c.status,
                )
            ).first()
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise

        if row is None:
            raise RecordNotFoundException("TEAM_REQUEST")

        return TeamRequestDTO(
            id=row.id,
            team_id=row.team_id,
            sender_user_id=row.sender_user_id,
            receiver_user_id=row.receiver_user_id,
            status=row.status,
        )

    def accept_team_request_and_assign_user(
        self,
        team_request_id: int,
    ) -> tuple[TeamRequestDTO, int]:
        existing_request = self.get_team_request_by_id(team_request_id)
        if existing_request is None:
            raise RecordNotFoundException("TEAM_REQUEST")

        try:
            accepted_row = self.db.execute(
                update(team_request_association)
                .where(team_request_association.c.id == team_request_id)
                .values(status=TeamRequestStatus.ACCEPTED)
                .returning(
                    team_request_association.c.id,
                    team_request_association.c.team_id,
                    team_request_association.c.sender_user_id,
                    team_request_association.c.receiver_user_id,
                    team_request_association.c.status,
                )
            ).first()

            if accepted_row is None:
                raise RecordNotFoundException("TEAM_REQUEST")

            self.db.execute(
                user_team_association.insert().values(
                    user_id=accepted_row.receiver_user_id,
                    team_id=accepted_row.team_id,
                )
            )

            deleted_other_pending_invitations = (
                self.db.execute(
                    update(team_request_association)
                    .where(
                        team_request_association.c.receiver_user_id
                        == accepted_row.receiver_user_id,
                        team_request_association.c.id != accepted_row.id,
                        team_request_association.c.status == TeamRequestStatus.PENDING,
                    )
                    .values(status=TeamRequestStatus.DELETED)
                ).rowcount
                or 0
            )

            self.db.commit()
        except Exception:
            self.db.rollback()
            raise

        accepted_request = TeamRequestDTO(
            id=accepted_row.id,
            team_id=accepted_row.team_id,
            sender_user_id=accepted_row.sender_user_id,
            receiver_user_id=accepted_row.receiver_user_id,
            status=accepted_row.status,
        )
        return accepted_request, deleted_other_pending_invitations

    def delete_team_with_associations(self, team_id: int) -> tuple[int, int]:
        try:
            deleted_team_requests = (
                self.db.execute(
                    delete(team_request_association).where(
                        team_request_association.c.team_id == team_id
                    )
                ).rowcount
                or 0
            )

            deleted_user_team_associations = (
                self.db.execute(
                    delete(user_team_association).where(
                        user_team_association.c.team_id == team_id
                    )
                ).rowcount
                or 0
            )

            self.db.execute(delete(Team).where(Team.id == team_id))
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise

        return deleted_team_requests, deleted_user_team_associations
