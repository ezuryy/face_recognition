from pydantic import BaseModel, Extra
from uuid import UUID
from typing import List


class CreateRequestResponse(BaseModel):
    success: str

    class Config:
        extra = Extra.allow
        orm_mode = True


class EmployeeResponse(BaseModel):
    name: str
    position: str
    department: str
    chief_id: UUID

    class Config:
        extra = Extra.allow
        orm_mode = True


class EmployeeListResponse(BaseModel):
    employees: List[EmployeeResponse]

    class Config:
        extra = Extra.allow
        orm_mode = True
