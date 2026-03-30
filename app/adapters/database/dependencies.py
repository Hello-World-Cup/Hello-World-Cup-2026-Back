from typing import Any, Callable
from sqlalchemy.orm import Session
from jose import JWTError, jwt  # type: ignore
from app.adapters.database.postgres.repositories.role_repository import RoleRepository
from app.adapters.routing.utils.granular_permissions import GranularFunctions
from app.domain.dtos.user_dto import UserDTO
from app.domain.enums import UserStatus
from app.ports.driven.database.postgres.role_repository import RoleRepositoryInterface
from fastapi import Depends, Header  # type: ignore

from app.core.use_case.test.delete_test import DeleteTestByIdHandler
from app.core.use_case.test.get_test import GetTestByIdHandler
from app.core.use_case.auth.register_user import RegisterUserHandler
from app.core.use_case.auth.login_user import LoginUserHandler
from app.core.use_case.auth.get_current_user import GetCurrentUserHandler
from app.core.use_case.auth.verify_email import VerifyEmailHandler
from app.adapters.database.postgres.repositories.test_repository import TestRepository
from app.adapters.database.postgres.repositories.user_repository import UserRepository
from app.adapters.database.postgres.connection import get_db
from app.adapters.supabase.supabase_connection import supabase_client
from app.adapters.supabase.supabase_storage import StorageBucketSupabase
from app.ports.driving.storage_bucket_interfaz import StorageBucketInterfaceABC

from app.core.use_case.bucket.upload_portrait import UploadPortraitHandler
from app.core.use_case.bucket.delete_portrait import DeletePortraitHandler
from app.core.use_case.bucket.upload_sponsor_logo import UploadSponsorLogoHandler
from app.core.use_case.bucket.upload_exercise import UploadExerciseHandler


from app.adapters.database.postgres.connection import SessionLocal
from app.adapters.database.postgres.repositories.team_repository import TeamRepository
from app.core.use_case.team.get_user_team import GetUserTeamHandler
from app.core.use_case.team.get_active_users import GetActiveUsersHandler

from app.domain.config import settings
from app.domain.exceptions.base_exceptions import (
    ForbiddenException,
    UnauthorizedException,
)


from app.adapters.database.postgres.repositories.refresh_token_repository import (
    RefreshTokenRepository,
)
from app.core.use_case.auth.refresh_access_token import RefreshAccessTokenHandler
from app.core.use_case.auth.signout import SignOutHandler
from app.adapters.email.gmail_smtp_sender import GmailSmtpSender

from app.adapters.routing.utils.context import user_context


# Repositories


def get_test_repository(db: Session) -> TestRepository:
    return TestRepository(db)


def get_user_repository(db: Session) -> UserRepository:
    return UserRepository(db)


def get_role_repository(db: Session) -> RoleRepository:
    return RoleRepository(db)


# Use cases


def get_test_by_id_handler(db: Session = Depends(get_db)) -> GetTestByIdHandler:
    return GetTestByIdHandler(get_test_repository(db))


def delete_test_by_id_handler(db: Session = Depends(get_db)) -> DeleteTestByIdHandler:
    return DeleteTestByIdHandler(get_test_repository(db))


def get_supabase_client() -> StorageBucketInterfaceABC:
    return StorageBucketSupabase(supabase_client())


def get_upload_portrait_handler(
    storage: StorageBucketInterfaceABC = Depends(get_supabase_client),
) -> UploadPortraitHandler:
    return UploadPortraitHandler(storage)


def get_delete_portrait_handler(
    storage: StorageBucketInterfaceABC = Depends(get_supabase_client),
) -> DeletePortraitHandler:
    return DeletePortraitHandler(storage)


def get_upload_sponsor_logo_handler(
    storage: StorageBucketInterfaceABC = Depends(get_supabase_client),
) -> UploadSponsorLogoHandler:
    return UploadSponsorLogoHandler(storage)


def get_upload_exercise_handler(
    storage: StorageBucketInterfaceABC = Depends(get_supabase_client),
) -> UploadExerciseHandler:
    return UploadExerciseHandler(storage)


def get_login_user_handler(db: Session = Depends(get_db)) -> LoginUserHandler:
    return LoginUserHandler(
        get_user_repository(db),
        get_refresh_token_repository(db),
    )


def get_refresh_token_repository(db: Session) -> RefreshTokenRepository:
    return RefreshTokenRepository(db)


def get_refresh_access_token_handler(
    db: Session = Depends(get_db),
) -> RefreshAccessTokenHandler:
    return RefreshAccessTokenHandler(
        get_refresh_token_repository(db),
        get_user_repository(db),
    )


def get_signout_handler(db: Session = Depends(get_db)) -> SignOutHandler:
    return SignOutHandler(get_refresh_token_repository(db))


def get_email_sender() -> GmailSmtpSender:
    return GmailSmtpSender()


def get_register_user_handler(db: Session = Depends(get_db)) -> RegisterUserHandler:
    return RegisterUserHandler(
        get_user_repository(db),
        get_role_repository(db),
        get_email_sender(),
    )


def get_current_user_handler(db: Session = Depends(get_db)) -> GetCurrentUserHandler:
    return GetCurrentUserHandler(get_user_repository(db))


def get_verify_email_handler(db: Session = Depends(get_db)) -> VerifyEmailHandler:
    return VerifyEmailHandler(get_user_repository(db))


def get_team_repository(db: Session = Depends(get_db)) -> TeamRepository:
    return TeamRepository(db)

def get_user_team_handler(
    team_repo: TeamRepository = Depends(get_team_repository)
) -> GetUserTeamHandler:
    return GetUserTeamHandler(team_repo)

def get_active_users_handler(
    team_repo: TeamRepository = Depends(get_team_repository)
) -> GetActiveUsersHandler:
    return GetActiveUsersHandler(team_repo)


# Authorization


async def get_current_user_payload(
    authorization: str | None = Header(None, alias="Authorization"),
) -> dict[str, Any]:
    if not authorization or not authorization.startswith("Bearer "):
        raise UnauthorizedException("Token not sent or invalid format")
    token = authorization.removeprefix("Bearer ").strip()
    if not token:
        raise UnauthorizedException("Token not sent or invalid format")
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload
    except JWTError:
        raise UnauthorizedException("Invalid or expired session")


async def set_authorized_user(
    user_payload=Depends(get_current_user_payload),
    db: Session = Depends(get_db),
) -> None:
    user_id = user_payload.get("sub")

    if not user_id:
        raise UnauthorizedException("Invalid token")

    repo = get_user_repository(db)
    user_context.set(repo.get_by_id(user_id))


def RequireRoles(allowed_codes: list[str], granular_requirements: list[str]) -> Callable[..., Any]:

    async def _authorize(
        db: Session = Depends(get_db),
        _=Depends(set_authorized_user),
    ) -> None:

        role_repo = get_role_repository(db)

        if not allowed_codes and not granular_requirements:
            return

        user = user_context.get()
        if not user or not user.role_id:
            raise UnauthorizedException("Authentication required")

        role = role_repo.get_by_id(user.role_id)

        if not role:
            raise UnauthorizedException("User role not found or invalid")
        
        if role.is_super_user:
            return

        if role.internal_code not in allowed_codes:
            raise ForbiddenException()

        granular_functions = GranularFunctions()

        for requirement in granular_requirements:
            callable = granular_functions.get_granular_function(requirement)

            if callable is not None:
                result = callable(user)

                if not result:
                    raise ForbiddenException()
    
    return _authorize
