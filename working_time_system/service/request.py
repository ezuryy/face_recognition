from uuid import UUID
from fastapi import Depends
from datetime import datetime

from working_time_system.repository import (
    RequestRepository,
    get_request_repository,
    EmployeeRepository,
    get_employee_repository
)
from working_time_system.utils import RequestStatus
from working_time_system.schema import MyRequestsRequestResponse


class RequestService:
    def __init__(self, request_repository: RequestRepository, employee_repository: EmployeeRepository):
        self._request_repository = request_repository
        self._employee_repository = employee_repository

    async def create_request(
            self, employee_id: UUID,
            event_type: str,
            from_dt: datetime,
            to_dt: datetime,
            content: str,
            status: RequestStatus
    ):
        return await self._request_repository.create_request(
            employee_id, event_type, from_dt, to_dt, content, status.name
        )

    async def get_user_requests(
            self,
            employee_id: UUID
    ) -> MyRequestsRequestResponse:
        return await self._request_repository.get_user_requests(employee_id)

    async def get_requests_for_user(
            self,
            chief_id: UUID
    ) -> MyRequestsRequestResponse:
        requests_with_id = await self._request_repository.get_requests_for_user(chief_id)
        return requests_with_id

    async def update_request(
            self,
            request_id: UUID,
            status: str
    ):
        await self._request_repository.update_request(request_id, status)

    async def get_chief_id_by_request_id(
            self,
            request_id: UUID
    ) -> UUID:
        chief_id = await self._request_repository.get_chief_id_by_request_id(request_id)
        return chief_id


async def get_request_service(
    request_repository: RequestRepository = Depends(get_request_repository),
    employee_repository: EmployeeRepository = Depends(get_employee_repository)
) -> RequestService:
    return RequestService(request_repository, employee_repository)
