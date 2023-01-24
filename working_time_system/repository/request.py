from uuid import UUID
from fastapi import Depends
from sqlalchemy import desc, select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from typing import Union

from working_time_system.db.models import Request, Employee
from working_time_system.db.connection import get_session


class RequestRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_request(
            self,
            employee_id: UUID,
            event_type: str,
            from_dt: datetime,
            to_dt: datetime,
            content: str,
            status: str
    ):
        query = insert(Request).values(
            employee_id=employee_id,
            event=event_type,
            from_dt=from_dt + timedelta(hours=12),
            to_dt=to_dt + timedelta(hours=12),
            content=content,
            status=status
        )
        await self._session.execute(query)
        await self._session.commit()

    async def get_user_requests(
            self,
            employee_id: UUID
    ):
        print(f'employee_id : {employee_id}, type : {type(employee_id)}')
        query = await self._session.execute(
            select(Request, Employee).join(
                Employee, Employee.id == Request.employee_id
            ).where(Employee.id == employee_id).order_by(desc(Request.from_dt))
        )
        entry = query.all()
        print(entry)
        return entry


    async def get_requests_for_user(
            self,
            chief_id: UUID
    ):
        query = await self._session.execute(
            select(Request, Employee).join(
                Employee, Employee.id == Request.employee_id
            ).where(Employee.chief_id == chief_id).order_by(desc(Request.from_dt))
        )
        entry = query.all()
        print(entry)
        return entry

    async def update_request(
            self,
            request_id: UUID,
            status: str
    ):
        query = await self._session.execute(
            select(Request).where(Request.id == request_id)
        )
        entry = query.scalars().first()
        print(entry)
        entry.status = status
        await self._session.commit()

    async def get_chief_id_by_request_id(
            self,
            request_id: UUID
    ) -> Union[UUID, None]:
        query = await self._session.execute(
            select(Employee, Request).join(
                Employee,
                Employee.id == Request.employee_id
            ).where(Request.id == request_id)
        )
        entry = query.scalars().first()
        print(entry)
        if entry is not None:
            return entry.chief_id
        return None


async def get_request_repository(session: AsyncSession = Depends(get_session)) -> RequestRepository:
    return RequestRepository(session=session)
