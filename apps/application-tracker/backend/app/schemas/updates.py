from typing import Literal
from pydantic import BaseModel
from datetime import datetime


class Updates(BaseModel):
    company_name: str
    job_title: str | None
    reference_number: str | None
    update_type: Literal[
        "application_received",
        "in_review",
        "missing_documents",
        "online_interview",
        "on_site_interview",
        "offer",
        "rejection",
        "withdrawn",
        "on_hold",
        "no_update",
        "other",
    ]
    contact_person: str | None
    contact_email: str | None
    short_summary: str | None
    confidence: float | None
    email_sent_date: datetime | None
