from fastapi import APIRouter

from api.routes.endpoints import endpoints
from utils.dttm import current_utc_str

######################################################
## Router for Health Checks
######################################################

health_checks_router = APIRouter(tags=["Health Checks"])


@health_checks_router.get(endpoints.PING)
def ping_api():
    return {
        "status": "success",
        "path": endpoints.PING,
        "utc": current_utc_str(),
    }
