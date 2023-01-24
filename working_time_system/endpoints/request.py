from uuid import UUID
from fastapi import APIRouter, Depends
from starlette import status
from datetime import datetime
from typing import Union, List, Tuple

from working_time_system.schema import CreateRequestResponse, MyRequestsRequestResponse
from working_time_system.service import RequestService, get_request_service
from working_time_system.utils import RequestStatus


api_router = APIRouter(tags=["Request"])


@api_router.post(
    "/create_request",
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
async def create_request(
    event_type: str,
    from_dt: str,
    to_dt: str,
    content: Union[str, None],
    request_service: RequestService = Depends(get_request_service),
) -> CreateRequestResponse:
    # TODO: create get_employee_id func
    employee_id = UUID('e6c40f1a-268d-43c5-ac5a-7ae274d0cda5')
    from_dt = datetime.strptime(from_dt, "%d.%m.%Y")
    to_dt = datetime.strptime(to_dt, "%d.%m.%Y")
    if content is None:
        content = ''
    await request_service.create_request(
        employee_id=employee_id,
        event_type=event_type,
        from_dt=from_dt,
        to_dt=to_dt,
        content=content,
        status=RequestStatus.sent
    )
    return CreateRequestResponse(success='Done')



@api_router.get(
    "/get_user_requests",
    status_code=status.HTTP_200_OK,
    response_model=MyRequestsRequestResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthorized",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Not found",
        },
    },
)
async def get_user_requests(
    employee_id: str,
    request_service: RequestService = Depends(get_request_service),
) -> MyRequestsRequestResponse:
    requests = await request_service.get_user_requests(UUID(employee_id))
    return MyRequestsRequestResponse(requests=requests)


@api_router.get(
    "/get_requests_for_user",
    status_code=status.HTTP_200_OK,
    response_model=MyRequestsRequestResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthorized",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Not found",
        },
    },
)
async def get_requests_for_user(
    employee_id: str,
    request_service: RequestService = Depends(get_request_service),
) -> MyRequestsRequestResponse:
    requests = await request_service.get_requests_for_user(UUID(employee_id))
    return MyRequestsRequestResponse(requests=requests)


@api_router.put(
    "/update_request/{request_id}",
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
async def update_request(
    request_id: str,
    new_status: str,
    request_service: RequestService = Depends(get_request_service),
) -> CreateRequestResponse:
    await request_service.update_request(UUID(request_id), new_status)
    return CreateRequestResponse(success='Done')

