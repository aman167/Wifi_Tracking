
import time
from database_setup import create_database, insert_initial_data
from employee_tracking import simulate_movement
from analysis import EmployeeAnalytics

def main():
    print("1. Setting up database...")
    conn = create_database()
    insert_initial_data(conn)
    conn.close()
    print("Database setup completed")
    
    print("\n2. Starting employee movement simulation...")
    # Simulate for 5 minutes
    simulate_movement(duration_seconds=300)
    print("Movement simulation completed")
    
    print("\n3. Generating analytics...")
    analytics = EmployeeAnalytics()
    
    # Generate store layout
    analytics.plot_store_layout()
    print("Store layout saved as 'store_layout.png'")
    
    # Generate time heatmap
    analytics.create_time_heatmap(time_window_minutes=5)
    print("Time heatmap saved as 'time_heatmap.png'")
    
    # Generate zone activity heatmap
    analytics.create_zone_heatmap(time_window_minutes=5)
    print("Zone activity heatmap saved as 'zone_heatmap.png'")
    
    print("\nAnalysis completed successfully")

if __name__ == "__main__":
    main()
