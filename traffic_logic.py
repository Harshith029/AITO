from typing import List
from datetime import datetime, timedelta
from models.traffic_models import (
    Location,
    TrafficDataRequest,
    OptimizedRouteRequest,
    OptimizedRouteResponse,
    RouteSegment,
    TrafficScore
)
import random

# Simulated in-memory storage for demo
traffic_data_storage: List[TrafficDataRequest] = []


# Store traffic data
def save_traffic_data(data: TrafficDataRequest) -> str:
    traffic_data_storage.append(data)
    return "Data stored successfully."


def calculate_congestion_score(data: TrafficDataRequest) -> float:
    score = data.vehicle_count * 1.2

    if data.weather == "rain":
        score += 20
    elif data.weather == "fog":
        score += 15
    elif data.weather == "clear":
        score -= 5

    if data.accident_reported:
        score += 25

    if data.school_zone:
        score += 10

    if data.event_nearby:
        score += 15

    return round(score, 2)

def determine_risk_level(score: float) -> str:
    if score < 30:
        return "Low"
    elif score < 60:
        return "Moderate"
    else:
        return "Severe"


def get_traffic_score_for_location(location: Location) -> TrafficScore:
    matched = [
        data for data in traffic_data_storage
        if round(data.location.latitude, 2) == round(location.latitude, 2)
        and round(data.location.longitude, 2) == round(location.longitude, 2)
    ]

    if not matched:
        score = random.uniform(10, 80)
    else:
        scores = [calculate_congestion_score(data) for data in matched]
        score = sum(scores) / len(scores)

    risk = determine_risk_level(score)

    return TrafficScore(
        location=location,
        score=score,
        risk_level=risk
    )


def simulate_route(user_id: str, current: Location, dest: Location) -> List[RouteSegment]:
    route = [
        RouteSegment(
            road_name="Main Road",
            duration_minutes=random.uniform(5, 15),
            congestion_level=random.choice(["Low", "Medium", "High"])
        ),
        RouteSegment(
            road_name="Second Street",
            duration_minutes=random.uniform(5, 10),
            congestion_level=random.choice(["Low", "Medium", "High"])
        ),
        RouteSegment(
            road_name="Expressway",
            duration_minutes=random.uniform(10, 20),
            congestion_level=random.choice(["Low", "Medium", "High"])
        )
    ]
    return route

def calculate_total_time(route: List[RouteSegment]) -> float:
    return round(sum(segment.duration_minutes for segment in route), 2)

def get_optimized_route(request: OptimizedRouteRequest) -> OptimizedRouteResponse:
    route = simulate_route(request.user_id, request.current_location, request.destination)
    total_time = calculate_total_time(route)

    delay_factor = 0
    for segment in route:
        if segment.congestion_level == "High":
            delay_factor += 5
        elif segment.congestion_level == "Medium":
            delay_factor += 2

    suggested_time = request.current_time + timedelta(minutes=delay_factor)

    return OptimizedRouteResponse(
        user_id=request.user_id,
        route=route,
        estimated_total_time=total_time + delay_factor,
        suggested_departure_time=suggested_time,
        notes="Suggested time includes delays due to congestion"
    )


def clear_traffic_data():
    traffic_data_storage.clear()

def count_records():
    return len(traffic_data_storage)

def fetch_latest_entries(n: int = 5) -> List[TrafficDataRequest]:
    return traffic_data_storage[-n:]

def dummy_bulk_insert(n: int = 100):
    for _ in range(n):
        dummy = TrafficDataRequest(
            location=Location(latitude=17.385, longitude=78.4867),
            vehicle_count=random.randint(10, 200),
            timestamp=datetime.now(),
            weather=random.choice(["rain", "clear", "fog"]),
            accident_reported=random.choice([True, False]),
            school_zone=random.choice([True, False]),
            event_nearby=random.choice([True, False])
        )
        save_traffic_data(dummy)


def is_peak_hour(current_time: datetime) -> bool:
    return 8 <= current_time.hour <= 10 or 17 <= current_time.hour <= 19

def adjust_route_for_weather(route: List[RouteSegment], weather: str) -> List[RouteSegment]:
    if weather == "rain":
        for segment in route:
            segment.duration_minutes += 3
    elif weather == "fog":
        for segment in route:
            segment.duration_minutes += 2
    return route

def adjust_route_for_school_zones(route: List[RouteSegment], near_school: bool) -> List[RouteSegment]:
    if near_school:
        for segment in route:
            if "School" in segment.road_name:
                segment.duration_minutes += 4
    return route

def average_score_nearby(latitude: float, longitude: float) -> float:
    scores = []
    for data in traffic_data_storage:
        if abs(data.location.latitude - latitude) < 0.01 and abs(data.location.longitude - longitude) < 0.01:
            scores.append(calculate_congestion_score(data))
    return sum(scores) / len(scores) if scores else random.uniform(20, 70)

def generate_report_summary() -> dict:
    return {
        "total_records": count_records(),
        "average_score": average_score_nearby(17.385, 78.4867),
        "recent_data": [data.dict() for data in fetch_latest_entries()]
    }


def is_night_time(current_time: datetime) -> bool:
    return current_time.hour < 6 or current_time.hour > 21

def adjust_score_for_night(score: float, current_time: datetime) -> float:
    if is_night_time(current_time):
        score += 10  # assume extra caution required
    return score

# Simulated integration to weather API (mocked)
def fetch_weather_data(location: Location) -> str:
    return random.choice(["rain", "clear", "fog"])

# Placeholder to sync with frontend

def format_route_for_frontend(route: List[RouteSegment]) -> List[dict]:
    return [{
        "road": segment.road_name,
        "duration": round(segment.duration_minutes, 2),
        "congestion": segment.congestion_level
    } for segment in route]

# Simulated logger

def log_event(event: str):
    print(f"[LOG {datetime.now()}] {event}")

# Placeholder analytics collector

def collect_analytics():
    data_points = [calculate_congestion_score(entry) for entry in traffic_data_storage]
    return {
        "max": max(data_points) if data_points else 0,
        "min": min(data_points) if data_points else 0,
        "avg": sum(data_points)/len(data_points) if data_points else 0
    }

# Final mock endpoint simulator

def simulate_api_health_check() -> dict:
    return {
        "status": "OK",
        "records": count_records(),
        "timestamp": datetime.now().isoformat()
    }
