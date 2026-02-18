from fastapi import APIRouter # type: ignore

default_router=APIRouter()

@default_router.get("/health")
def get_health() -> dict[str, str]:
    return {"status": "alive"}
