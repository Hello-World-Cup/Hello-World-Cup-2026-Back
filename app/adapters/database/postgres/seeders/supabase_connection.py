# app/adapters/database/storage/supabase_connection.py

import os
from supabase import create_client, Client
from functools import lru_cache


@lru_cache()
def supabase_client() -> Client:

    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    if not url or not key:
        raise ValueError(
            "Faltan variables de entorno para Supabase: "
            "SUPABASE_URL y SUPABASE_SERVICE_ROLE_KEY deben estar definidas."
        )
    
    return create_client(url, key)