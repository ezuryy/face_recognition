from fastapi import APIRouter, Depends
from starlette import status

from working_time_system.service import WorkTimeService, get_work_time_service


api_router = APIRouter(tags=["Face recognition"])


@api_router.post(
    "/face_recognition",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthorized",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Not found",
        },
    },
)
async def write_face_recognition_to_csv(
    name: str,
    event_type: str,
    work_time_service: WorkTimeService = Depends(get_work_time_service),
) -> None:
    await work_time_service.write_event_to_csv(name, event_type)

