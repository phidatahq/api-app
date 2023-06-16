from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.settings import api_settings
from api.routes.v1_router import v1_router
from utils.log import logger


def create_app() -> FastAPI:
    """Create a FastAPI App

    Returns:
        FastAPI: FastAPI App
    """

    # Create FastAPI App
    app: FastAPI = FastAPI(
        title=api_settings.title,
        version=api_settings.version,
        docs_url="/docs" if api_settings.docs_enabled else None,
        redoc_url="/redoc" if api_settings.docs_enabled else None,
        openapi_url="/openapi.json" if api_settings.docs_enabled else None,
    )

    # Add v1 router
    app.include_router(v1_router)

    # Add Middlewares
    app.add_middleware(
        CORSMiddleware,
        allow_origins=api_settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app

# Create FastAPI app
app = create_app()

if api_settings.create_tables:
    # Create tables in database
    from db.tables import Base
    from db.session import db_engine

    Base.metadata.create_all(bind=db_engine)
    logger.info("Created tables")
