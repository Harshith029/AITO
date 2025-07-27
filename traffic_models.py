from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Location(BaseModel):
    latitude: float
    longitude: float

class TrafficDataRequest(BaseModel):
    location: Location
    vehicle_count: int = Field(..., ge=0)
    timestamp: datetime
    weather: Optional[str] = None
    accident_reported: Optional[bool] = False
    school_zone: Optional[bool] = False
    event_nearby: Optional[bool] = False

class OptimizedRouteRequest(BaseModel):
    user_id: str
    current_location: Location
    destination: Location
    current_time: datetime

class RouteSegment(BaseModel):
    road_name: str
    duration_minutes: float
    congestion_level: str 

class OptimizedRouteResponse(BaseModel):
    user_id: str
    route: List[RouteSegment]
    estimated_total_time: float
    suggested_departure_time: datetime
    notes: Optional[str] = None

class TrafficScore(BaseModel):
    location: Location
    score: float
    risk_level: str  
