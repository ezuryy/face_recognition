from fastapi import APIRouter, Depends
from starlette import status

from working_time_system.schema import ReportResponse
from working_time_system.service import ReportService, get_report_service


api_router = APIRouter(tags=["Report generator"])


@api_router.get(
    "/get_report",
    status_code=status.HTTP_200_OK,
    response_model=ReportResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthorized",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Not found",
        },
    },
)
async def get_report(
    department: str,
    month: int,
    year: int,
    report_service: ReportService = Depends(get_report_service),
) -> ReportResponse:
    report_path = await report_service.get_report(department, month, year)
    return ReportResponse(report_path=report_path)
