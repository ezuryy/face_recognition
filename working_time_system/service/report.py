from fastapi import Depends
from uuid import UUID

from working_time_system.repository import (
    ReportRepository,
    get_report_repository,
    EmployeeRepository,
    get_employee_repository
)


class ReportService:
    def __init__(self, report_repository: ReportRepository, employee_repository: EmployeeRepository):
        self._report_repository = report_repository
        self._employee_repository = employee_repository

    async def get_report(self, employee_id: UUID, department: str, month: int, year: int) -> str:
        # department = self._employee_repository.get_subordinate_department(employee_id)
        # if department is not None:
        #     report_path = await self._report_repository.get_report(department, month, year)
        # else:
        #     report_path = await report_service.get_report_for_employee(department, int(month), int(year))
        return await self._report_repository.get_report(employee_id, department, month, year)


async def get_report_service(
    report_repository: ReportRepository = Depends(get_report_repository),
    employee_repository: EmployeeRepository = Depends(get_employee_repository),
) -> ReportService:
    return ReportService(report_repository, employee_repository)
