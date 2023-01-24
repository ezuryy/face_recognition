from fastapi import Depends

from working_time_system.repository.work_time import WorkTimeRepository, get_work_time_repository
from working_time_system.repository.request import RequestRepository, get_request_repository


class WorkTimeService:
    def __init__(self, work_time_repository: WorkTimeRepository, request_repository: RequestRepository):
        self._work_time_repository = work_time_repository
        self._payments_repository = request_repository

    async def write_event_to_csv(self, name: str, event_type: str):
        return await self._work_time_repository.write_event_to_csv(name, event_type)


async def get_work_time_service(
    work_time_repository: WorkTimeRepository = Depends(get_work_time_repository),
    request_repository: RequestRepository = Depends(get_request_repository),
) -> WorkTimeService:
    return WorkTimeService(work_time_repository, request_repository)
