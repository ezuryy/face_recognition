from fastapi import APIRouter, Depends
from starlette import status
from typing import Optional

from working_time_system.schema import CreateRequestResponse
from working_time_system.service import EmployeeService, get_employee_service
from working_time_system.schema import EmployeeListResponse


api_router = APIRouter(tags=["Employee"])


@api_router.post(
    "/create_employee",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthorized",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Not found",
        },
    },
)
async def create_employee(
    name: str,
    position: str,
    department: str,
    chief_name: str,
    employee_service: EmployeeService = Depends(get_employee_service),
) -> CreateRequestResponse:
    await employee_service.create_employee(
        name=name,
        position=position,
        department=department,
        chief_name=chief_name,
    )
    return CreateRequestResponse(success='Done')



@api_router.get(
    "/get_employees",
    status_code=status.HTTP_200_OK,
    response_model=EmployeeListResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthorized",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Not found",
        },
    },
)
async def get_employees(
    department: str,
    employee_service: EmployeeService = Depends(get_employee_service),
) -> EmployeeListResponse:
    employees = await employee_service.get_employees(department)
    return EmployeeListResponse(employees=employees)


@api_router.put(
    "/update_employee",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthorized",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Not found",
        },
    },
)
async def update_employee(
        name: str,
        position: Optional[str] = None,
        department: Optional[str] = None,
        chief_name: Optional[str] = None,
        login: Optional[str] = None,
        password: Optional[str] = None,
        employee_service: EmployeeService = Depends(get_employee_service),
) -> CreateRequestResponse:
    await employee_service.update_employee(
        name=name,
        position=position,
        department=department,
        chief_name=chief_name,
        login=login,
        password=password
    )
    return CreateRequestResponse(success='Done')

