from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.settings import api_settings
from api.routes.v1_routes import v1_router


# Create FastAPI App
app: FastAPI = FastAPI(
    title=api_settings.title,
    version=api_settings.version,
    docs_url="/docs" if api_settings.docs_enabled else None,
    redoc_url="/redoc" if api_settings.docs_enabled else None,
    openapi_url="/openapi.json" if api_settings.docs_enabled else None,
)

# Create APIRouter for "v1" routes. This helps gracefully migrate as the API grows.
# https://fastapi.tiangolo.com/tutorial/bigger-applications/#apirouter
app.include_router(v1_router)

# Add CORSMiddleware
# https://fastapi.tiangolo.com/tutorial/cors/#use-corsmiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=api_settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
