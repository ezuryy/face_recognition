from uuid import UUID
from fastapi import Depends
from typing import Union

from working_time_system.repository import (
    RequestRepository,
    get_request_repository,
    EmployeeRepository,
    get_employee_repository
)


class EmployeeService:
    def __init__(self, request_repository: RequestRepository, employee_repository: EmployeeRepository):
        self._request_repository = request_repository
        self._employee_repository = employee_repository

    async def get_user_id_by_name(self, name: str) -> Union[UUID, None]:
        return await self._employee_repository.get_user_id_by_name(name)

    async def get_name_by_user_id(self, employee_id: UUID) -> Union[str, None]:
        return await self._employee_repository.get_name_by_user_id(employee_id)

    async def create_employee(
            self,
            name: str,
            position: str,
            department: str,
            chief_name: str
    ):
        chief_id = await self._employee_repository.get_user_id_by_name(chief_name)
        return await self._employee_repository.create_employee(name, position, department, chief_id)

    async def get_employees(self, department: str):
        return await self._employee_repository.get_employees(department)

    async def update_employee(
            self,
            name: str,
            position: Union[str, None],
            department: Union[str, None],
            chief_name: Union[str, None],
            login: Union[str, None],
            password: Union[str, None]
    ):
        await self._employee_repository.update_employee(name, position, department, chief_name, login, password)

    async def check_login(self, login: str) -> bool:
        return await self._employee_repository.check_login(login)

    async def check_password(self, login: str, password: str) -> Union[UUID, None]:
        return await self._employee_repository.check_password(login, password)


async def get_employee_service(
    request_repository: RequestRepository = Depends(get_request_repository),
    employee_repository: EmployeeRepository = Depends(get_employee_repository),
) -> EmployeeService:
    return EmployeeService(request_repository, employee_repository)
