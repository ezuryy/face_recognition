from uuid import UUID, uuid4
from fastapi import Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Union

from working_time_system.db.models import Employee
from working_time_system.db.connection import get_session


class EmployeeRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_user_id_by_name(self, name: str) -> Union[UUID, None]:
        query = await self._session.execute(select(Employee.id).where(Employee.name == name))
        entry = query.scalars().first()
        return entry

    async def get_name_by_user_id(self, employee_id: UUID) -> Union[str, None]:
        query = await self._session.execute(select(Employee.name).where(Employee.id == employee_id))
        entry = query.scalars().first()
        return entry

    async def create_employee(
            self,
            name: str,
            position: str,
            department: str,
            chief_id: Union[UUID, None]
    ):
        if chief_id is None:
            employee_id = uuid4()
            query = insert(Employee).values(
                id=employee_id,
                name=name,
                position=position,
                department=department,
                chief_id=employee_id
            )
        else:
            query = insert(Employee).values(
                name=name,
                position=position,
                department=department,
                chief_id=chief_id
            )
        await self._session.execute(query)
        await self._session.commit()

    async def get_employees(
            self,
            department: str
    ):
        query = await self._session.execute(select(Employee).where(Employee.department == department))
        entry = query.scalars().all()
        return entry

    async def update_employee(
            self,
            name: str,
            position: Union[str, None],
            department: Union[str, None],
            chief_name: Union[str, None],
            login: Union[str, None],
            password: Union[str, None]
    ):
        query = await self._session.execute(
            select(Employee).where(Employee.name == name)
        )
        entry = query.scalars().first()
        entry.position = position if position is not None else entry.position
        entry.department = department if department is not None else entry.department
        if chief_name is not None:
            chief_id = await self.get_user_id_by_name(chief_name)
            entry.chief_id = chief_id
        entry.login = login if login is not None else entry.login
        entry.password = password if password is not None else entry.password
        await self._session.commit()

    async def check_login(self, login: str) -> bool:
        query = await self._session.execute(select(Employee).where(Employee.login == login))
        entry = query.all()
        if len(entry):
            return True
        return False

    async def check_password(self, login: str, password: str) -> Union[UUID, None]:
        query = await self._session.execute(select(Employee).where(Employee.login == login))
        entry = query.scalars().first()
        if entry.password == password:
            return entry.id
        return None

    async def get_subordinate_department(self, employee_id: UUID) -> Union[str, None]:
        query = await self._session.execute(select(Employee.department).where(Employee.chief_id == employee_id))
        entry = query.scalars().first()
        return entry



async def get_employee_repository(session: AsyncSession = Depends(get_session)) -> EmployeeRepository:
    return EmployeeRepository(session=session)
