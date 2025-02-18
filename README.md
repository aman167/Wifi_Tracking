
# Employee Movement Tracking System

This project implements a WiFi-based employee tracking system for retail stores. It simulates employee movements, tracks their locations using WiFi signal strength, and provides analytical insights through visualizations.

## Features

- Real-time employee position tracking using WiFi triangulation
- Store zone mapping and management
- Movement analysis and visualization
- Time spent analysis per zone
- Employee transition tracking
- Interactive heatmaps and store layouts

## System Requirements

- Python 3.8 or higher
- SQLite3
- Required Python packages (listed in requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/employee-tracking-system.git
cd employee-tracking-system
```

2. Create and activate a virtual environment (optional but recommended):
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Project Structure

- `database_setup.py`: Database creation and initialization
- `employee_tracking.py`: Real-time employee tracking simulation
- `analysis.py`: Data analysis and visualization
- `main.py`: Pipeline execution of all components
- `requirements.txt`: Required Python packages
- `README.md`: Project documentation

## Running the System

1. Ensure all requirements are installed and you're in the project directory

2. Run the main script:
```bash
python main.py
```

This will:
- Set up the SQLite database
- Initialize sample data
- Run a 5-minute movement simulation
- Generate analytics and visualizations

## Output Files

The system generates two visualization files:
- `store_layout.png`: Shows the store layout with defined zones
- `time_heatmap.png`: Displays employee time spent in different zones

## Database Schema

### Employees Table
- employee_id (PRIMARY KEY)
- name
- role
- device_mac
- created_at

### Zones Table
- zone_id (PRIMARY KEY)
- name
- x_min
- x_max
- y_min
- y_max

### Movement_Logs Table
- log_id (PRIMARY KEY)
- employee_id (FOREIGN KEY)
- timestamp
- x_coord
- y_coord
- zone_id (FOREIGN KEY)

## Customization

You can modify various parameters in the code:
- Simulation duration in `main.py`
- Store dimensions and zones in `database_setup.py`
- Movement patterns in `employee_tracking.py`
- Analysis time windows in `analysis.py`

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.
