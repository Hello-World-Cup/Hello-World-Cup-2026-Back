from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from app.core.use_case.team.get_user_team import GetUserTeamHandler
from app.core.use_case.team.get_active_users import GetActiveUsersHandler
from app.adapters.database.dependencies import (
    get_user_team_handler,
    get_active_users_handler,
    RequireRoles
)
from app.adapters.routing.utils.decorators import format_response
from app.adapters.routing.utils.context import user_context 


team_router = APIRouter(prefix="/team", tags=["team"])


@team_router.get("")
@format_response
async def get_user_team(
    handler: GetUserTeamHandler = Depends(get_user_team_handler),
    _: str = Depends(RequireRoles([], [])),  
) -> Any:
    current_user = user_context.get()
    if not current_user or not hasattr(current_user, 'id'):
        raise HTTPException(401, "unauthenticated user")
    
    return handler.execute(str(current_user.id))


@team_router.get("/users")
@format_response
async def get_active_users(
    handler: GetActiveUsersHandler = Depends(get_active_users_handler),
    _: str = Depends(RequireRoles([], [])),  
) -> Any:
    return handler.execute()