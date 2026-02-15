import logging
import sys

from fastapi import FastAPI # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore

from app.domain.config import settings

# Routes
from app.adapters.routing.fastapi.routers.default_router import default_router
from app.adapters.routing.fastapi.routers.test_router import test_router


def init_app(app: FastAPI) -> FastAPI:
    setup_routes(app)
    setup_middleware(app)
    setup_logger()
    return app

def setup_routes(app: FastAPI) -> None:
    app.include_router(default_router)
    app.include_router(test_router)
    # Additional routers can be included here

def setup_middleware(app: FastAPI) -> None:
    origins = ["*"] # TODO: Update with specific origins in production

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )

def setup_logger() -> None:
    logging_levels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    log_level = logging_levels.get(settings.LOGGING_LEVEL, logging.DEBUG)

    # Get the root logger
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Create handler for stdout (for INFO and below)
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(formatter)

    # Create handler for stderr (for WARNING and above)
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.WARNING)
    stderr_handler.setFormatter(formatter)

    # Add handlers to the root logger
    logger.addHandler(stdout_handler)
    logger.addHandler(stderr_handler)

    # Set level for other loggers
    logging.getLogger("pymongo").setLevel(logging.WARNING)

    logging.info("Logs are set up.")
