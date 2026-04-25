import logging
from app.adapters.database.postgres.seeders.development_data_seeder import (
    DevelopmentDataSeeder,
)
from app.adapters.routing.utils.response import ResponseFormatter
from app.domain.exceptions.base_exceptions import DomainException
from fastapi import FastAPI  # type: ignore

from app.adapters.routing.fastapi.config import init_app
from app.adapters.database.postgres.connection import SessionLocal
from app.domain.feature_flags import FeatureFlags
from app.adapters.database.postgres.seeders.test_seeder import TestSeeder
from app.adapters.database.postgres.seeders.initialize_models import initialize_tables
from fastapi import Request  # type: ignore
from fastapi.responses import JSONResponse  # type: ignore
from fastapi.encoders import jsonable_encoder  # type: ignore

app = FastAPI(title="HWC SERVER", version="1.0.0")


@app.exception_handler(Exception)
async def universal_exception_handler(request: Request, exc: Exception):
    error_message = "An unexpected error occurred"
    error_code = "INTERNAL_SERVER_ERROR"

    if isinstance(exc, DomainException):
        error_code = getattr(exc, "error_code", "DOMAIN_ERROR")
        error_message = str(exc)

    response_model = ResponseFormatter.format_response(
        success=False, status_code=error_code, error=error_message
    )
    clean_response = jsonable_encoder(response_model)

    return JSONResponse(
        status_code=401,
        content=clean_response,
    )


init_app(app)


@app.on_event("startup")
async def startup_events() -> None:
    logging.getLogger("uvicorn").info("Starting web server...")

    try:
        initialize_tables()

        if FeatureFlags().is_development:
            logging.getLogger("uvicorn").info("Running in development mode")
            TestSeeder(SessionLocal()).run(
                FeatureFlags().clear_existing_data_for_development
            )
            DevelopmentDataSeeder(SessionLocal()).run(
                FeatureFlags().clear_existing_data_for_development
            )

        logging.getLogger("uvicorn").info("Initialization complete")

    finally:
        pass


@app.on_event("shutdown")
async def shutdown_event() -> None:
    logging.getLogger("uvicorn").info("Shutting down server")
