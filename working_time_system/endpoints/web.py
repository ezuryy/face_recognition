from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from datetime import datetime
from uuid import UUID
import pytz

from working_time_system.service import (
    RequestService,
    get_request_service,
    ReportService,
    get_report_service,
    EmployeeService,
    get_employee_service
)
from working_time_system.utils import RequestStatus

api_router = APIRouter()
templates = Jinja2Templates(directory="public/")


@api_router.get("/")
async def root():
    return FileResponse("public/create_auth.html")


@api_router.get("/index")
async def index(
        request: Request,
        employee_id: UUID,
        employee_service: EmployeeService = Depends(get_employee_service)
):
    employee_name = await employee_service.get_name_by_user_id(employee_id)
    return templates.TemplateResponse("index.html", context={
        'request': request, 'employee_id': employee_id, 'employee_name': employee_name
    })


@api_router.get("/create_absence")
async def create_absence(
        request: Request,
        employee_id: UUID
):
    return templates.TemplateResponse("create_absence.html", context={
        'request': request, 'employee_id': employee_id
    })


@api_router.get("/apply_auth")
async def apply_auth(
        request: Request,
        employee_id: UUID
):
    return templates.TemplateResponse("apply_auth.html", context={
        'request': request, 'employee_id': employee_id
    })


@api_router.get("/apply_absence")
async def apply_absence(
        request: Request,
        employee_id: UUID,
        request_service: RequestService = Depends(get_request_service)
):
    data = await request_service.get_requests_for_user(employee_id)
    return templates.TemplateResponse("apply_absence.html", context={
        'request': request, 'employee_id': employee_id, 'data': data
    })


@api_router.get("/look_over_tabel")
async def look_over_tabel(
        request: Request,
        employee_id: UUID
):
    return templates.TemplateResponse("look_over_tabel.html", context={
        'request': request, 'employee_id': employee_id
    })


@api_router.post("/create_absence")
async def create_absence(
        request: Request,
        employee_id: UUID,
        event_type=Form(), from_dt=Form(), to_dt=Form(), content=Form(),
        request_service: RequestService = Depends(get_request_service)
):
    print(f'"ФИО": {employee_id}, "Тип": event_type, "Дата начала": from_dt, "Дата окончания": to_dt, "Коммент": content')

    from_dt = datetime.strptime(from_dt, "%Y-%m-%d")
    to_dt = datetime.strptime(to_dt, "%Y-%m-%d")
    await request_service.create_request(employee_id, event_type, from_dt, to_dt, content, RequestStatus.sent)
    return templates.TemplateResponse("create_absence.html", context={
        'request': request, 'employee_id': employee_id
    })


@api_router.post("/apply_auth")
async def apply_auth(
        request: Request,
        login=Form(), password=Form(),
        employee_service: EmployeeService = Depends(get_employee_service)
):
    if not employee_service.check_login(login):
        return FileResponse("public/apply_auth.html")
    employee_id = await employee_service.check_password(login, password)
    if employee_id is not None:
        employee_name = await employee_service.get_name_by_user_id(employee_id)
        return templates.TemplateResponse("index.html", context={
            'request': request, 'employee_id': employee_id, 'employee_name': employee_name
        })
    return FileResponse("public/apply_auth.html")


@api_router.post("/look_over_tabel")
async def look_over_tabel(
        request: Request,
        employee_id: UUID,
        department=Form(),
        month=Form(),
        year=Form(),
        report_service: ReportService = Depends(get_report_service),
):
    print({"Подразделение": department, "Месяц": month, "Год": year})
    report_path = await report_service.get_report(employee_id, department, int(month), int(year))
    return FileResponse(path=report_path, filename=report_path)


@api_router.post("/update_request_status")
async def update_request_status(
        request: Request,
        request_id=Form(),
        status=Form(),

        request_service: RequestService = Depends(get_request_service)):
    if status == 'Принять':
        status = RequestStatus.ok.name
    else:
        status = RequestStatus.canceled.name
    await request_service.update_request(request_id=UUID(request_id), status=status)
    curr_boss_id = await request_service.get_chief_id_by_request_id(request_id)
    data = await request_service.get_requests_for_user(curr_boss_id)
    return templates.TemplateResponse("apply_absence.html", context={
        'request': request, 'employee_id': curr_boss_id, 'data': data
    })


@api_router.get("/show_absence")
async def show_absence(
        request: Request,
        employee_id: UUID,
        request_service: RequestService = Depends(get_request_service)
):
    data = await request_service.get_user_requests(employee_id)
    return templates.TemplateResponse("show_absence.html", context={
        'request': request, 'employee_id': employee_id, 'data': data
    })
