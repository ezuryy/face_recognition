from pydantic import BaseModel


class ReportResponse(BaseModel):
    report_path: str
