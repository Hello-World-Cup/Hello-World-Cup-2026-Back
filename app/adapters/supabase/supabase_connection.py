from supabase import create_client, Client # type: ignore
from functools import lru_cache
from app.domain.config import settings 



@lru_cache()
def supabase_client() -> Client:

    url = settings.SUPABASE_URL
    key = settings.SUPABASE_SERVICE_ROLE_KEY
    
    if not url or not key:
        raise ValueError(
            "Environment variables are missingW: "
            "SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are not defined."
        )
    
    return create_client(url, key)