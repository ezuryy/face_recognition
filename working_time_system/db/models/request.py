from sqlalchemy import Column, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID, TEXT
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from working_time_system.db import DeclarativeBase
from working_time_system.db.models import Employee

import enum


class Event(enum.Enum):
    weekend = 'Выходной'
    turnout = 'Явка'
    vacation = 'Отпуск'
    business_trip = 'Командировка'
    sick = 'Больничный'
    strike = 'Забастовка'


class RequestStatus(enum.Enum):
    ok = 'Одобрено'
    canceled = 'Отказано'
    sent = 'Не просмотрено'


class Request(DeclarativeBase):
    __tablename__ = "request"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
        unique=True,
        doc="Unique id of the employee",
    )
    employee_id = Column(UUID(as_uuid=True), ForeignKey("employee.id"))
    event = Column(Enum(Event))
    from_dt = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False,
        doc="Start date of event",
    )
    to_dt = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False,
        doc="End date of event",
    )
    content = Column(
        TEXT,
        nullable=False)
    status = Column(
        Enum(RequestStatus)
    )

    employee = relationship(Employee)

    def __repr__(self):
        columns = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        return f'<{self.__tablename__}: {", ".join(map(lambda x: f"{x[0]}={x[1]}", columns.items()))}>'
