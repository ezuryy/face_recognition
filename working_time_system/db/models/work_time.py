from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP, VARCHAR, FLOAT
from sqlalchemy.sql import func

from working_time_system.db import DeclarativeBase


class WorkTime(DeclarativeBase):
    __tablename__ = "work_time"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
        unique=True,
        doc="work_time id",
    )
    date = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False,
        doc="Date",
    )
    name = Column(
        VARCHAR(70),
        unique=False,
        nullable=False,
        doc="Name of the employee",
    )
    work_hours = Column(
        FLOAT(precision=2),
        nullable=False,
    )

    def __repr__(self):
        columns = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        return f'<{self.__tablename__}: {", ".join(map(lambda x: f"{x[0]}={x[1]}", columns.items()))}>'
