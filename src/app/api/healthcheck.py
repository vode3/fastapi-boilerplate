from fastapi import APIRouter
from fastapi import status
from pydantic import BaseModel

from app.api.common.responses import OkResponse


healthcheck_router = APIRouter(prefix="/health", tags=["healthcheck"])


class HealthcheckResponse(BaseModel):
    status: bool = True


@healthcheck_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=HealthcheckResponse,
)
async def healthcheck_endpoint() -> OkResponse[HealthcheckResponse]:
    return OkResponse(content=HealthcheckResponse(status=True))
