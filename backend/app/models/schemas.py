from pydantic import BaseModel

from typing import List, Dict

from datetime import datetime


class AcceptanceRequest(BaseModel):

    tender_id: str

    officer_id: str

    accepted_standards: List[str]

    verified: bool = True

    certification_verifications: Dict[str, bool] = {}


class AcceptanceResponse(BaseModel):

    status: str

    pdf_url: str

    timestamp: datetime