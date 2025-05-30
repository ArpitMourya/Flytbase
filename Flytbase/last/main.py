from conflict_checker import load_primary_mission, load_simulated_drones, check_conflicts

def main():
    primary = load_primary_mission(r"D:\Flytbase\data\primary_mission.json")
    simulated = load_simulated_drones(r"D:\Flytbase\data\simulated_drones.json")
    conflicts = check_conflicts(primary, simulated)
    
    print("Conflicts found:")
    for c in conflicts:
        print(c)

if __name__ == "__main__":
    main()
