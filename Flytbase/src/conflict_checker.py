from typing import List, Dict, Any, Tuple
from datetime import datetime
from pydantic import BaseModel
import json
from math import sqrt

# Data Models
class Waypoint(BaseModel):
    x: float
    y: float
    z: float
    timestamp: datetime

class Mission(BaseModel):
    time_window: List[datetime]
    waypoints: List[Waypoint]

class FlightPath(BaseModel):
    drone_id: str
    waypoints: List[Waypoint]

# Data Loading Functions
def load_primary_mission(path: str) -> Mission:
    with open(path, "r") as f:
        data = json.load(f)
    return Mission(**data)

def load_simulated_drones(path: str) -> List[FlightPath]:
    with open(path, "r") as f:
        data = json.load(f)
    # If data is a list of dicts (one per drone)
    if isinstance(data, list):
        return [FlightPath(**drone) for drone in data]
    # If data is a dict with "drones" key
    elif "drones" in data:
        return [FlightPath(**drone) for drone in data["drones"]]
    else:
        raise ValueError("Unexpected format for simulated drones JSON.")

def load_test_case(file_path: str) -> Tuple[Mission, List[FlightPath]]:
    with open(file_path, "r") as f:
        data = json.load(f)
    primary = Mission(**data["primary_drone"])
    simulated = [FlightPath(**d) for d in data["simulated_drones"]]
    return primary, simulated

# Conflict Checking
def euclidean_distance(wp1: Waypoint, wp2: Waypoint) -> float:
    return sqrt((wp1.x - wp2.x)**2 + (wp1.y - wp2.y)**2 + (wp1.z - wp2.z)**2)

def check_conflicts(primary: Mission, others: List[FlightPath], spatial_thresh=5.0, temporal_thresh=2.0):
    conflicts = []
    for wp_primary in primary.waypoints:
        for drone in others:
            for wp_other in drone.waypoints:
                dt = abs((wp_primary.timestamp - wp_other.timestamp).total_seconds())
                if dt <= temporal_thresh:
                    dist = euclidean_distance(wp_primary, wp_other)
                    if dist <= spatial_thresh:
                        conflicts.append({
                            "primary_time": wp_primary.timestamp,
                            "other_drone": drone.drone_id,
                            "other_time": wp_other.timestamp,
                            "distance": dist,
                            "location": {
                                "x": wp_primary.x,
                                "y": wp_primary.y,
                                "z": wp_primary.z
                            }
                        })
    return conflicts

def check_deconfliction(
    primary_mission: Mission,
    simulated_flights: List[FlightPath],
    spatial_thresh: float = 5.0,
    temporal_thresh: float = 2.0
) -> Dict[str, Any]:
    """
    Checks for spatial and temporal conflicts between the primary mission and simulated flights.
    Returns a status dict.
    """
    conflicts_raw = []
    for wp_primary in primary_mission.waypoints:
        for drone in simulated_flights:
            for wp_other in drone.waypoints:
                dt = abs((wp_primary.timestamp - wp_other.timestamp).total_seconds())
                if dt <= temporal_thresh:
                    dist = euclidean_distance(wp_primary, wp_other)
                    if dist <= spatial_thresh:
                        conflicts_raw.append({
                            "primary_time": wp_primary.timestamp.isoformat(),
                            "other_drone": drone.drone_id,
                            "other_time": wp_other.timestamp.isoformat(),
                            "distance": dist
                        })
    conflicts = [
        {
            "location": {"x": c["primary_time"].x, "y": c["primary_time"].y, "z": c["primary_time"].z}
            if hasattr(c["primary_time"], "x") else
            {"x": 0, "y": 0, "z": 0},
            "other_drone": c["other_drone"],
            "primary_time": str(c["primary_time"]),
            "other_time": str(c["other_time"]),
            "distance": c["distance"]
        }
        for c in conflicts_raw
    ]
    if conflicts:
        return {"status": "conflict", "details": conflicts}
    else:
        return {"status": "clear"}
