# Flytbase UAV Deconfliction

This project provides a framework for detecting and visualizing spatial and temporal conflicts between a primary UAV mission and multiple simulated drone flights.

## Features

- **Conflict Detection:** Identifies conflicts based on configurable spatial and temporal thresholds.
- **3D Visualization:** Uses Plotly to visualize drone paths and conflict points.
- **Test Scenarios:** Includes basic conflict scenarios for validation.

## Setup

1. **Clone the repository**  
   ```sh
   git clone <repo-url>
   cd Flytbase
   ```

2. **Install dependencies**  
   ```sh
   pip install -r requirements.txt
   ```

## Run

To run the simulation and visualization:

```sh
cd src
python main.py
```

## Configuration

Modify `config.yaml` to adjust mission parameters, conflict thresholds, and other settings.

## Visualizing Results

Results are saved in the `results` folder. Open `index.html` in a browser to view the 3D visualization.

## Testing

Run unit tests to validate functionality:

```sh
pytest tests
```

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for discussion.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the need for safe UAV operations in complex airspaces.
- Utilizes Plotly for advanced 3D visualizations.