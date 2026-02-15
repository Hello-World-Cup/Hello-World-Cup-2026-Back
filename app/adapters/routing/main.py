import logging
from fastapi import FastAPI  # type: ignore

from app.adapters.routing.fastapi.config import init_app
from app.adapters.database.postgres.connection import SessionLocal
from app.domain.feature_flags import FeatureFlags
from app.adapters.database.postgres.seeders.test_seeder import TestSeeder
from app.adapters.database.postgres.seeders.initialize_models import initialize_tables

app = FastAPI(title="HWC SERVER", version="1.0.0")
init_app(app)

@app.on_event("startup")
async def startup_events() -> None:
    logging.getLogger("uvicorn").info("Starting web server...")

    try:
        initialize_tables()

        if FeatureFlags().is_development:
            logging.getLogger("uvicorn").info("Running in development mode")
            TestSeeder(SessionLocal()).run()
        
        logging.getLogger("uvicorn").info("Initialization complete")
    finally:
        pass

@app.on_event("shutdown")
async def shutdown_event() -> None:
    logging.getLogger("uvicorn").info("Shutting down server")