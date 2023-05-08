from fastapi import APIRouter

from api.routes.health_checks import health_checks_router
from api.routes.users import users_router


v1_router = APIRouter(prefix="/v1")
v1_router.include_router(health_checks_router)
v1_router.include_router(users_router)
