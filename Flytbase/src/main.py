from conflict_checker import load_primary_mission, load_simulated_drones, check_conflicts, check_deconfliction
from visualization import plot3d_conflict_scene

def main():
    primary = load_primary_mission(r"D:\Flytbase\data\primary_mission.json")
    simulated = load_simulated_drones(r"D:\Flytbase\data\simulated_drones.json")

    # Prepare data for visualization
    primary_waypoints = [wp.dict() for wp in primary.waypoints]
    simulated_drones = [
        {"drone_id": drone.drone_id, "waypoints": [wp.dict() for wp in drone.waypoints]}
        for drone in simulated
    ]

    # Find conflicts and prepare for visualization
    conflicts_raw = check_conflicts(primary, simulated)
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

    # Visualize
    plot3d_conflict_scene(primary_waypoints, simulated_drones, conflicts)

    # (Optional) Print summary
    print("\nDeconfliction summary:")
    print(check_deconfliction(primary, simulated))

if __name__ == "__main__":
    main()
