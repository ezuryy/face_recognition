from fastapi import APIRouter
from starlette import status

from working_time_system.schema import PingResponse


api_router = APIRouter(tags=["Health check"])


@api_router.get(
    "/health_check/ping",
    response_model=PingResponse,
    status_code=status.HTTP_200_OK,
)
async def health_check() -> PingResponse:
    return PingResponse()
