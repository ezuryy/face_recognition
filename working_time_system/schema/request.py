from pydantic import BaseModel, Extra
from datetime import datetime
from typing import List
from uuid import UUID

from working_time_system.utils import Event, RequestStatus


class CreateRequestResponse(BaseModel):
    success: str

    class Config:
        extra = Extra.allow
        orm_mode = True


class RequestResponse(BaseModel):
    id: UUID
    employee_id: UUID
    event: Event
    from_dt: datetime
    to_dt: datetime
    content: str
    status: RequestStatus

    class Config:
        allow_population_by_field_name = True
        orm_mode = True
        use_enum_values = True
        arbitrary_types_allowed = True


class MyRequestsRequestResponse(BaseModel):
    requests: List[RequestResponse]

    class Config:
        allow_population_by_field_name = True
        orm_mode = True
        use_enum_values = True
        arbitrary_types_allowed = True
