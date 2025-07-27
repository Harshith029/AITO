from pydantic import BaseModel
from typing import Optional

class SmartRouteRequest(BaseModel):
    source: str
    destination: str
    time: str  
    preference: str
    notes: Optional[str] = None
