from working_time_system.endpoints.health_check import api_router as health_check_router
from working_time_system.endpoints.face_recog import api_router as face_recog_router
from working_time_system.endpoints.report import api_router as report_router
from working_time_system.endpoints.request import api_router as request_router
from working_time_system.endpoints.web import api_router as web_router
from working_time_system.endpoints.employee import api_router as api_employee

list_of_routes = [
    health_check_router,
    face_recog_router,
    report_router,
    request_router,
    web_router,
    api_employee,
]


__all__ = [
    "list_of_routes",
]
