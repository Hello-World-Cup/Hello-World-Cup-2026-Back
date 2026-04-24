from fastapi import APIRouter # type: ignore

default_router = APIRouter(tags=["Health"])

@default_router.get("/health")
def get_health() -> dict[str, str]:
    return {"status": "alive"}
