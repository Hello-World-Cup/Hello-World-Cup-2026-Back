import os
from supabase import create_client, Client
from functools import lru_cache
from app.domain.config import settings 



@lru_cache()
def supabase_client() -> Client:

    url = settings.getenv("SUPABASE_URL")
    key = settings.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    if not url or not key:
        raise ValueError(
            "Faltan variables de entorno para Supabase: "
            "SUPABASE_URL y SUPABASE_SERVICE_ROLE_KEY deben estar definidas."
        )
    
    return create_client(url, key)