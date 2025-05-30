from typing import List
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
                            "distance": dist
                        })
    return conflicts
