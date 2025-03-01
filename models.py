# models.py
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class CashFlowRecord(BaseModel):
    raw_text: Optional[str] = None
    amount: float
    category: str  # Expected: "rent", "electricity", "phone", "subscriptions", "other"

class DigitalFootprint(BaseModel):
    tiktok: Optional[Dict[str, Any]] = None
    # Extend with other platforms as needed

class Application(BaseModel):
    general_info: Dict[str, Any]
    cash_flow: List[CashFlowRecord]
    digital_footprint: Optional[DigitalFootprint] = None
    official_documents: Optional[Dict[str, Any]] = None
    history_data: Dict[str, Any]  # Should include "eligible": 0 or 1