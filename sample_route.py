from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import List

router = APIRouter()

# Simple Ping Test
@router.get("/api/ping")
def ping():
    return {"message": "pong from AITO backend"}

class SmartRouteRequest(BaseModel):
    from_location: str
    to_location: str
    bus_stops: List[str]
    time_of_day: str
    day_of_week: str
    weather: str
    is_rainy: bool
    is_school_time: bool

@router.post("/api/smart-route")
async def get_smart_route(request: SmartRouteRequest):
    # Placeholder for AI logic
    print("Received Smart Route Request:", request.dict())

    # Simulated optimized path logic
    simulated_route = [request.from_location] + request.bus_stops + [request.to_location]

    return {
        "from": request.from_location,
        "to": request.to_location,
        "route": simulated_route,
        "time": 24 
    }
