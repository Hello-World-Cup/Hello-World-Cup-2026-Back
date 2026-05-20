from __future__ import annotations

from datetime import datetime
import re

from pydantic import BaseModel, Field, field_validator  # type: ignore

from app.domain.dtos.user_dto import UserResponseDTO
from app.domain.enums import ProgrammingLanguage, TeamRequestStatus


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
    votes_qty: int | None = Field(default=None)
    description: str |None = Field(default=None)

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
            votes_qty=getattr(orm_obj, "votes_qty", None),
            description=getattr(orm_obj, "description", None),
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
    name: str = Field(..., min_length=1, max_length=30)
    description: str = Field(..., min_length=1, max_length=100)


class CreateTeamResponseDTO(BaseModel):
    message: str = Field(default="Team created successfully")
    team: TeamResponseDTO = Field(...)


class UploadTeamRepositoryLinkInputDTO(BaseModel):
    repository_link: str = Field(..., min_length=1, max_length=255)

    @field_validator("repository_link")
    @classmethod
    def validate_github_repository_link(cls, value: str) -> str:
        normalized_value = value.strip()
        github_repository_pattern = (
            r"^https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:\.git)?/?$"
        )
        if not re.fullmatch(github_repository_pattern, normalized_value):
            raise ValueError("repository_link must be a valid GitHub repository URL")
        return normalized_value


class UploadTeamRepositoryLinkResponseDTO(BaseModel):
    message: str = Field(default="Repository link uploaded successfully")
    team: TeamResponseDTO = Field(...)


class SendTeamInvitationsInputDTO(BaseModel):
    usernames: list[str] = Field(..., min_length=1, description="Usernames to invite")


class AssignProjectEvaluatorInputDTO(BaseModel):
    user_id: int = Field(
        ..., gt=0, description="User identifier to set as project evaluator"
    )


class AssignProjectEvaluatorResponseDTO(BaseModel):
    message: str = Field(default="Project evaluator assigned successfully")
    team: TeamResponseDTO = Field(...)


class UpdateTeamScoreFeedbackInputDTO(BaseModel):
    score: int | None = Field(default=None, description="Score to assign to the team")
    feedback: str | None = Field(default=None, description="Feedback text for the team")


class UpdateTeamScoreFeedbackResponseDTO(BaseModel):
    message: str = Field(default="Team updated successfully")
    team: TeamResponseDTO = Field(...)


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


class TeamDisplayDTO(BaseModel):
    id: int = Field(...)
    name: str = Field(...)
    logo: str | None = Field(default=None)
    score: int | None = Field(default=None)
    standing_position: int | None = Field(default=None)
    cloud_repo_link: str | None = Field(default=None)
    status: int = Field(default=0)
    feedback: str | None = Field(default=None)
    edition_id: int = Field(...)
    category_name: str = Field(...)
    evaluation_id: int | None = Field(default=None)
    evaluation_file_url: str | None = Field(default=None)
    assigned_evaluator_username: str | None = Field(default=None)
    project_evaluator_username: str | None = Field(default=None)
    votes_qty: int | None = Field(default=None)


class TeamListItemDisplayDTO(BaseModel):
    team: TeamDisplayDTO = Field(...)
    leader: UserResponseDTO | None = Field(default=None)
    members_count: int = Field(default=0)


class ListTeamsDisplayResponseDTO(BaseModel):
    message: str = Field(default="Teams retrieved successfully")
    teams: list[TeamListItemDisplayDTO] = Field(default_factory=list)


class TeamTableRowDTO(BaseModel):
    team_name: str = Field(...)
    leader_name: str | None = Field(default=None)
    evaluator: str | None = Field(default=None)
    repository_link: str | None = Field(default=None)
    status: str = Field(...)
    score: int | None = Field(default=None)
    feedback: str | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)


class ListTeamsTableResponseDTO(BaseModel):
    message: str = Field(default="Teams table retrieved successfully")
    teams: list[TeamTableRowDTO] = Field(default_factory=list)


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
    id: int
    username: str
    name: str
    programming_language: ProgrammingLanguage | None = None
    github_profile: str | None = None


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
