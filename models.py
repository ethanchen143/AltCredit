from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class CashFlowRecord(BaseModel):
    time: int # number of days before the application
    amount: float
    category: str  # Expected: "rent", "electricity", "phone", "subscriptions", "other"

class DigitalFootprint(BaseModel):
    tiktok: Optional[Dict[str, Any]] = None

class User(BaseModel):
    email: str
    hashed_password: str
    general_info: Dict[str, Any]
    cash_flow: Optional[List[CashFlowRecord]] = None
    digital_footprint: Optional[DigitalFootprint] = None
    official_documents: Optional[str] = None
    history_data: Optional[Dict[str, Any]] = None