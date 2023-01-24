from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID, VARCHAR
from sqlalchemy.sql import func

from working_time_system.db import DeclarativeBase


class Employee(DeclarativeBase):
    __tablename__ = "employee"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
        unique=True,
        doc="Unique id of the employee",
    )
    name = Column(
        VARCHAR(70),
        unique=False,
        nullable=False,
        doc="Name of the employee",
    )
    position = Column(
        VARCHAR(70),
        unique=False,
        nullable=False,
        doc="Position of the employee",
    )
    department = Column(
        VARCHAR(70),
        unique=False,
        nullable=False,
        doc="Department of the employee",
    )
    chief_id = Column(
        UUID(as_uuid=True),
        unique=False,
        nullable=False,
        doc="Id of the employee chief",
    )
    login = Column(
        VARCHAR(70),
        unique=False,
        nullable=True,
        doc="Login of the employee",
    )
    password = Column(
        VARCHAR(70),
        unique=False,
        nullable=True,
        doc="Password of the employee",
    )

    def __repr__(self):
        columns = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        return f'<{self.__tablename__}: {", ".join(map(lambda x: f"{x[0]}={x[1]}", columns.items()))}>'
