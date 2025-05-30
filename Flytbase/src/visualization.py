import plotly.graph_objs as go

def plot3d_conflict_scene(primary_waypoints, simulated_drones, conflicts=None):
    fig = go.Figure()

    # Plot primary drone path
    fig.add_trace(go.Scatter3d(
        x=[wp["x"] for wp in primary_waypoints],
        y=[wp["y"] for wp in primary_waypoints],
        z=[wp["z"] for wp in primary_waypoints],
        mode='lines+markers',
        name='Primary Drone',
        line=dict(color='blue', width=4),
        marker=dict(size=4)
    ))

    # Mark start and end for primary drone
    fig.add_trace(go.Scatter3d(
        x=[primary_waypoints[0]["x"]],
        y=[primary_waypoints[0]["y"]],
        z=[primary_waypoints[0]["z"]],
        mode='markers',
        name='Primary Start',
        marker=dict(size=10, color='green', symbol='circle')
    ))
    fig.add_trace(go.Scatter3d(
        x=[primary_waypoints[-1]["x"]],
        y=[primary_waypoints[-1]["y"]],
        z=[primary_waypoints[-1]["z"]],
        mode='markers',
        name='Primary End',
        marker=dict(size=10, color='orange', symbol='diamond')
    ))

    # Plot simulated drones and their start/end
    for drone in simulated_drones:
        waypoints = drone["waypoints"]
        fig.add_trace(go.Scatter3d(
            x=[wp["x"] for wp in waypoints],
            y=[wp["y"] for wp in waypoints],
            z=[wp["z"] for wp in waypoints],
            mode='lines+markers',
            name=drone["drone_id"],
            line=dict(width=2),
            marker=dict(size=3)
        ))
        # Start point
        fig.add_trace(go.Scatter3d(
            x=[waypoints[0]["x"]],
            y=[waypoints[0]["y"]],
            z=[waypoints[0]["z"]],
            mode='markers',
            name=f'{drone["drone_id"]} Start',
            marker=dict(size=8, color='green', symbol='circle')
        ))
        # End point
        fig.add_trace(go.Scatter3d(
            x=[waypoints[-1]["x"]],
            y=[waypoints[-1]["y"]],
            z=[waypoints[-1]["z"]],
            mode='markers',
            name=f'{drone["drone_id"]} End',
            marker=dict(size=8, color='orange', symbol='diamond')
        ))

    # Highlight conflict points as red dots (not crosses)
    if conflicts:
        fig.add_trace(go.Scatter3d(
            x=[c["location"]["x"] for c in conflicts],
            y=[c["location"]["y"] for c in conflicts],
            z=[c["location"]["z"] for c in conflicts],
            mode='markers',
            name='Conflicts',
            marker=dict(size=10, color='red', symbol='circle')
        ))

    fig.update_layout(
        title="3D UAV Deconfliction Visualization",
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Altitude (Z)'
        ),
        legend=dict(x=0, y=1),
        margin=dict(l=0, r=0, b=0, t=40)
    )

    fig.show()