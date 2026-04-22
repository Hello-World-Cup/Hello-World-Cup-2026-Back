from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field  # type: ignore

from app.domain.dtos.user_dto import UserResponseDTO
from app.domain.enums import TeamRequestStatus


class TeamResponseDTO(BaseModel):
    id: int = Field(...)
    name: str = Field(...)
    logo: str | None = Field(default=None)
    score: int | None = Field(default=None)
    standing_position: int | None = Field(default=None)
    cloud_repo_link: str | None = Field(default=None)
    status: int = Field(default=0)
    feedback: str | None = Field(default=None)
    edition_id: int = Field(...)
    category_id: int = Field(...)
    evaluation_id: int | None = Field(default=None)
    assigned_evaluator_id: int | None = Field(default=None)
    project_evaluator_id: int | None = Field(default=None)

    @classmethod
    def from_orm(cls, orm_obj: object) -> "TeamResponseDTO":
        return cls(
            id=getattr(orm_obj, "id"),
            name=getattr(orm_obj, "name"),
            logo=getattr(orm_obj, "logo", None),
            score=getattr(orm_obj, "score", None),
            standing_position=getattr(orm_obj, "standing_position", None),
            cloud_repo_link=getattr(orm_obj, "cloud_repo_link", None),
            status=getattr(orm_obj, "status", 0),
            feedback=getattr(orm_obj, "feedback", None),
            edition_id=getattr(orm_obj, "edition_id"),
            category_id=getattr(orm_obj, "category_id"),
            evaluation_id=getattr(orm_obj, "evaluation_id", None),
            assigned_evaluator_id=getattr(orm_obj, "assigned_evaluator_id", None),
            project_evaluator_id=getattr(orm_obj, "project_evaluator_id", None),
        )


class TeamRequestDTO(BaseModel):
    id: int = Field(...)
    team_id: int = Field(...)
    sender_user_id: int = Field(...)
    receiver_user_id: int = Field(...)
    status: TeamRequestStatus = Field(...)


class TeamInvitationSummaryDTO(BaseModel):
    team_request_id: int = Field(...)
    team_id: int = Field(...)
    team_name: str = Field(...)
    sender_user_id: int = Field(...)
    sender_username: str = Field(...)
    status: TeamRequestStatus = Field(...)


class CreateTeamInputDTO(BaseModel):
    category_id: int = Field(..., gt=0, description="Category identifier")


class CreateTeamResponseDTO(BaseModel):
    message: str = Field(default="Team created successfully")
    team: TeamResponseDTO = Field(...)


class SendTeamInvitationsInputDTO(BaseModel):
    usernames: list[str] = Field(..., min_length=1, description="Usernames to invite")


class SendTeamInvitationsResponseDTO(BaseModel):
    message: str = Field(default="Invitations processed successfully")
    team_id: int = Field(...)
    created_requests: list[TeamRequestDTO] = Field(default_factory=list)
    not_found_usernames: list[str] = Field(default_factory=list)
    not_confirmed_usernames: list[str] = Field(default_factory=list)
    usernames_with_team: list[str] = Field(default_factory=list)
    already_invited_usernames: list[str] = Field(default_factory=list)
    duplicated_usernames: list[str] = Field(default_factory=list)
    self_invitation_usernames: list[str] = Field(default_factory=list)


class DeleteTeamInvitationResponseDTO(BaseModel):
    message: str = Field(default="Invitation deleted successfully")
    team_request_id: int = Field(...)
    status: TeamRequestStatus = Field(...)


class ListMyTeamInvitationsResponseDTO(BaseModel):
    message: str = Field(default="Pending invitations retrieved successfully")
    invitations: list[TeamInvitationSummaryDTO] = Field(default_factory=list)


class AcceptTeamInvitationResponseDTO(BaseModel):
    message: str = Field(default="Invitation accepted successfully")
    team_request_id: int = Field(...)
    team: TeamResponseDTO = Field(...)
    status: TeamRequestStatus = Field(...)
    deleted_other_pending_invitations: int = Field(default=0)


class TeamListItemDTO(BaseModel):
    team: TeamResponseDTO = Field(...)
    leader: UserResponseDTO | None = Field(default=None)
    members_count: int = Field(default=0)


class ListTeamsResponseDTO(BaseModel):
    message: str = Field(default="Teams retrieved successfully")
    teams: list[TeamListItemDTO] = Field(default_factory=list)


class TeamDetailDTO(BaseModel):
    team: TeamResponseDTO = Field(...)
    leader: UserResponseDTO | None = Field(default=None)
    members: list[UserResponseDTO] = Field(default_factory=list)
    members_count: int = Field(default=0)


class GetTeamDetailResponseDTO(BaseModel):
    message: str = Field(default="Team retrieved successfully")
    team: TeamDetailDTO = Field(...)


class DeleteTeamResponseDTO(BaseModel):
    message: str = Field(default="Team deleted successfully")
    team_id: int = Field(...)
    deleted_team_requests: int = Field(...)
    deleted_user_team_associations: int = Field(...)


class UserListDTO(BaseModel):
    username: str
    email: str
    name: str

class TeamMemberDTO(BaseModel):
    user_id: str
    username: str
    email: str
    name: str
    status: str


class GetUserTeamResponseDTO(BaseModel):
    team_id: str
    team_name: str
    edition_id: str
    edition_name: str
    status: int = Field(default=0)
    feedback: str | None = Field(default=None)
    assigned_evaluator_id: int | None = Field(default=None)
    project_evaluator_id: int | None = Field(default=None)
    created_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)
    deleted_members: list[TeamMemberDTO] = Field(default_factory=list)
    pending_members: list[TeamMemberDTO] = Field(default_factory=list)
    accepted_members: list[TeamMemberDTO] = Field(default_factory=list)
