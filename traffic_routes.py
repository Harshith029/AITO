from fastapi import APIRouter, HTTPException, Query, Body
from typing import List, Optional, Dict
from pydantic import BaseModel
from datetime import datetime, time
import random

router = APIRouter(prefix="/traffic", tags=["Traffic Management"])


class Coordinate(BaseModel):
    latitude: float
    longitude: float

class TrafficDensity(BaseModel):
    road_id: str
    density: float  
    timestamp: datetime

class AlternateRoute(BaseModel):
    route_id: str
    path: List[str]
    estimated_time: float  
    reason: Optional[str]

class PublicEvent(BaseModel):
    name: str
    start_time: datetime
    end_time: datetime
    affected_roads: List[str]

class RouteRequest(BaseModel):
    current_location: Coordinate
    destination: Coordinate
    mode: str  
    time_of_day: Optional[str] = "day"  
    events: Optional[List[PublicEvent]] = []



ROADS = {
    "main_road": {"density": 0.8, "length": 4.2},
    "school_road": {"density": 0.5, "length": 2.5},
    "bypass_road": {"density": 0.3, "length": 5.0},
    "narrow_street": {"density": 0.2, "length": 1.2},
    "college_road": {"density": 0.6, "length": 3.0},
    "market_road": {"density": 0.9, "length": 1.8}
}

EVENTS = [
    PublicEvent(
        name="School Closing",
        start_time=datetime(2025, 7, 26, 12, 30),
        end_time=datetime(2025, 7, 26, 13, 30),
        affected_roads=["school_road"]
    ),
    PublicEvent(
        name="Friday Market",
        start_time=datetime(2025, 7, 26, 17, 0),
        end_time=datetime(2025, 7, 26, 21, 0),
        affected_roads=["market_road"]
    )
]

# Helper Functions

def is_event_active(event: PublicEvent, current_time: datetime) -> bool:
    return event.start_time <= current_time <= event.end_time

def adjust_density_for_event(density: float, active: bool) -> float:
    return min(1.0, density + 0.3) if active else density

def estimate_time(length: float, density: float, mode: str) -> float:
    base_speed = {"walk": 5, "bus": 30, "car": 40}
    speed = base_speed.get(mode, 30) * (1 - density)
    if speed <= 0:
        speed = 1
    return round((length / speed) * 60, 2)

def generate_alternate_routes(
    request: RouteRequest, current_time: datetime
) -> List[AlternateRoute]:
    routes = []

    for road_id, road_info in ROADS.items():
        density = road_info["density"]
        length = road_info["length"]

        # Check for events
        affected = any(
            road_id in e.affected_roads and is_event_active(e, current_time)
            for e in request.events
        )
        updated_density = adjust_density_for_event(density, affected)
        time_est = estimate_time(length, updated_density, request.mode)

        reason = "Event Impact" if affected else "Traffic Data"

        routes.append(AlternateRoute(
            route_id=road_id,
            path=[road_id],
            estimated_time=time_est,
            reason=reason
        ))

    return sorted(routes, key=lambda r: r.estimated_time)


# API Endpoints

@router.post("/smart-routes", response_model=List[AlternateRoute])
async def get_smart_routes(request: RouteRequest = Body(...)):
    """
    Returns smart alternate public transport routes considering live traffic, events, and road type.
    """
    current_time = datetime.now()
    final_routes = generate_alternate_routes(request, current_time)

    if not final_routes:
        raise HTTPException(status_code=404, detail="No routes found.")

    return final_routes

@router.get("/density", response_model=Dict[str, float])
async def get_current_traffic_density():
    """
    Returns the current density of all monitored roads.
    """
    current_time = datetime.now()
    traffic_data = {}

    for road_id, info in ROADS.items():
        is_affected = any(
            is_event_active(e, current_time) and road_id in e.affected_roads
            for e in EVENTS
        )
        updated_density = adjust_density_for_event(info["density"], is_affected)
        traffic_data[road_id] = round(updated_density, 2)

    return traffic_data

@router.get("/events", response_model=List[PublicEvent])
async def get_active_events():
    """
    Returns a list of currently active public events affecting traffic.
    """
    now = datetime.now()
    return [e for e in EVENTS if is_event_active(e, now)]

@router.get("/health")
async def health_check():
    """
    Health check endpoint for AITO Traffic Routes.
    """
    return {"status": "AITO Traffic Route module is live "}


@router.get("/debug/route-summary")
async def debug_route_summary(
    mode: str = Query("bus"),
    time_of_day: str = Query("day")
):
    """
    Returns a summary of travel times for each road based on current mode.
    """
    summaries = []
    now = datetime.now()

    for road_id, info in ROADS.items():
        is_affected = any(
            is_event_active(e, now) and road_id in e.affected_roads
            for e in EVENTS
        )
        updated_density = adjust_density_for_event(info["density"], is_affected)
        time_taken = estimate_time(info["length"], updated_density, mode)

        summaries.append({
            "road": road_id,
            "density": round(updated_density, 2),
            "eta": time_taken,
            "event_impact": is_affected
        })

    return summaries