from conflict_checker import load_test_case, check_conflicts, check_deconfliction
from visualization import plot3d_conflict_scene

def run_test(test_file):
    primary, simulated = load_test_case(test_file)
    print(f"\n=== Testing {test_file} ===")
    conflicts_raw = check_conflicts(primary, simulated)
    print("Conflicts found:")
    for c in conflicts_raw:
        print(c)
    print("Deconfliction summary:")
    print(check_deconfliction(primary, simulated))

    # Visualization (optional)
    primary_waypoints = [wp.dict() for wp in primary.waypoints]
    simulated_drones = [
        {"drone_id": drone.drone_id, "waypoints": [wp.dict() for wp in drone.waypoints]}
        for drone in simulated
    ]
    conflicts = [
        {
            "location": c["location"],  # Use the location directly
            "other_drone": c["other_drone"],
            "primary_time": str(c["primary_time"]),
            "other_time": str(c["other_time"]),
            "distance": c["distance"]
        }
        for c in conflicts_raw
    ]
    plot3d_conflict_scene(primary_waypoints, simulated_drones, conflicts)

if __name__ == "__main__":
    import os
    base = r"D:\Flytbase\basic_conflicts"
    for fname in ["head_on.json", "crossing_paths.json", "overtaking.json", "parallel_flights.json"]:
        run_test(os.path.join(base, fname))