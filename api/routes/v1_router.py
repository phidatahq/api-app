from fastapi import APIRouter

from api.routes.status_routes import status_router
from api.routes.user_routes import users_router


v1_router = APIRouter(prefix="/v1")
v1_router.include_router(status_router)
v1_router.include_router(users_router)
