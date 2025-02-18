
import sqlite3
import numpy as np
from datetime import datetime
import time

class EmployeeTracker:
    def __init__(self, db_path='retail_tracking.db'):
        self.db_path = db_path
        self.access_points = np.array([
            [10, 5],   # AP1
            [40, 5],   # AP2
            [25, 25]   # AP3
        ])
    
    def connect_db(self):
        return sqlite3.connect(self.db_path)
    
    def get_zone_id(self, x, y, cursor):
        cursor.execute("""
            SELECT zone_id FROM zones 
            WHERE x_min <= ? AND x_max >= ? 
            AND y_min <= ? AND y_max >= ?
        """, (x, x, y, y))
        zone = cursor.fetchone()
        return zone[0] if zone else None
    
    def simulate_wifi_signal(self, true_position):
        # Simulate RSSI values based on distance from access points
        distances = np.linalg.norm(self.access_points - true_position, axis=1)
        # Convert distance to RSSI (simplified model)
        rssi = -40 - 20 * np.log10(distances)  # Basic path loss model
        # Add some noise
        rssi += np.random.normal(0, 2, len(rssi))
        return rssi
    
    def estimate_position(self, rssi_values):
        # Simplified trilateration
        # Convert RSSI to estimated distances
        distances = 10 ** ((-40 - rssi_values) / 20)
        
        # Basic centroid algorithm
        weights = 1 / distances
        weights = weights / np.sum(weights)
        
        estimated_position = np.sum(self.access_points * weights[:, np.newaxis], axis=0)
        return estimated_position
    
    def track_employee(self, employee_id, true_position):
        """
        Track an employee's position and update the database
        true_position: [x, y] coordinates (in meters)
        """
        conn = self.connect_db()
        cursor = conn.cursor()
        
        # Simulate WiFi signals
        rssi_values = self.simulate_wifi_signal(true_position)
        
        # Estimate position from RSSI values
        estimated_position = self.estimate_position(rssi_values)
        
        # Get current zone
        zone_id = self.get_zone_id(estimated_position[0], estimated_position[1], cursor)
        
        # Log movement
        cursor.execute("""
            INSERT INTO movement_logs (employee_id, timestamp, x_coord, y_coord, zone_id)
            VALUES (?, ?, ?, ?, ?)
        """, (employee_id, datetime.now(), estimated_position[0], estimated_position[1], zone_id))
        
        conn.commit()
        conn.close()
        
        return estimated_position, zone_id

def simulate_movement(duration_seconds=60):
    tracker = EmployeeTracker()
    
    # Initial positions for each employee
    employee_positions = {
        i: np.random.rand(2) * [50, 30] for i in range(1, 6)
    }
    
    start_time = time.time()
    while time.time() - start_time < duration_seconds:
        for emp_id, position in employee_positions.items():
            # Simulate random movement
            movement = np.random.normal(0, 0.5, 2)  # Random walk
            new_position = np.clip(position + movement, [0, 0], [50, 30])
            employee_positions[emp_id] = new_position
            
            # Track the new position
            tracker.track_employee(emp_id, new_position)
        
        time.sleep(1)  # Update every second

if __name__ == "__main__":
    print("Starting employee movement simulation...")
    simulate_movement()
    print("Simulation completed")
