

# Reflection & Justification

## Design Decisions & Architecture

- **Modular Structure:** The codebase is organized into modules for conflict checking, visualization, and scenario testing. This separation allows for easy maintenance and extensibility.
- **Data Models:** Pydantic models (`Waypoint`, `Mission`, `FlightPath`) ensure robust parsing and validation of input data, reducing errors from malformed JSON.
- **Scenario Flexibility:** The system supports both real mission data and synthetic test cases, making it suitable for both development and demonstration.

## Spatial and Temporal Conflict Checks

- **Spatial Check:** The Euclidean distance between waypoints is computed. If the distance between a primary drone waypoint and any simulated drone waypoint is less than or equal to the spatial threshold (default: 5 meters), a potential conflict is flagged.
- **Temporal Check:** The absolute time difference between waypoints is calculated. If this difference is within the temporal threshold (default: 2 seconds), the conflict is considered valid.
- **Combined Logic:** Only waypoints that are both spatially and temporally close are marked as conflicts.

## AI Integration

- **No AI Used:** The current implementation uses deterministic, rule-based logic for conflict detection. No machine learning or AI algorithms are integrated at this stage.

## Testing Strategy & Edge Cases

- **Test Cases:** The `basic_conflicts` folder contains scenarios for head-on, crossing, overtaking, and parallel flights. Each scenario is run and visualized via `test_basic_conflicts.py`.
- **Edge Cases Considered:**
  - Drones with no overlapping time windows.
  - Drones flying at different altitudes.
  - Multiple drones with intersecting paths at different times.
  - Drones with identical waypoints but different timestamps.
- **Visualization:** Conflicts are visually confirmed in 3D, aiding manual validation.

## Scaling to Real-World Data

To handle tens of thousands of drones and real-time data:
- **Performance Optimization:**
  - **Spatial Indexing:** Use spatial data structures (e.g., k-d trees, R-trees) to quickly find nearby waypoints.
  - **Temporal Binning:** Index waypoints by time to limit comparisons to relevant intervals.
  - **Parallel Processing:** Distribute conflict checks across multiple CPU cores or machines.
- **Streaming Data:** Integrate with message queues or streaming platforms for real-time ingestion and processing.
- **Robust Data Handling:** Implement error handling for missing or malformed data, and support for incremental updates.
- **Visualization:** For large-scale scenarios, aggregate conflicts and provide summary statistics or heatmaps instead of plotting every waypoint.

---

This design provides a solid foundation for both research and practical UAV deconfliction, and can be extended for real-world, large-scale deployments.