
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import numpy as np

class EmployeeAnalytics:
    def __init__(self, db_path='retail_tracking.db'):
        self.db_path = db_path
    
    def connect_db(self):
        return sqlite3.connect(self.db_path)
    
    def get_movement_data(self, start_time=None, end_time=None):
        conn = self.connect_db()
        
        query = """
            SELECT m.*, e.name, e.role, z.name as zone_name,
                   z.x_min, z.x_max, z.y_min, z.y_max
            FROM movement_logs m
            JOIN employees e ON m.employee_id = e.employee_id
            LEFT JOIN zones z ON m.zone_id = z.zone_id
        """
        
        if start_time and end_time:
            query += " WHERE m.timestamp BETWEEN ? AND ?"
            df = pd.read_sql_query(query, conn, params=(start_time, end_time))
        else:
            df = pd.read_sql_query(query, conn)
        
        conn.close()
        return df
    
    def plot_store_layout(self):
        conn = self.connect_db()
        zones_df = pd.read_sql_query("SELECT * FROM zones", conn)
        conn.close()
        
        plt.figure(figsize=(15, 10))
        for _, zone in zones_df.iterrows():
            # Plot zone boundaries
            plt.fill([zone.x_min, zone.x_max, zone.x_max, zone.x_min],
                    [zone.y_min, zone.y_min, zone.y_max, zone.y_max],
                    alpha=0.3)
            
            # Add zone name in center of each zone
            plt.text((zone.x_min + zone.x_max)/2,
                    (zone.y_min + zone.y_max)/2,
                    zone.name,
                    horizontalalignment='center',
                    verticalalignment='center',
                    fontsize=12,
                    fontweight='bold')
        
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.title('Store Layout with Zones', fontsize=14, pad=20)
        plt.xlabel('Length (meters)', fontsize=12)
        plt.ylabel('Width (meters)', fontsize=12)
        plt.savefig('store_layout.png', bbox_inches='tight', dpi=300)
        plt.close()
    
    def create_time_heatmap(self, time_window_minutes=60):
        end_time = datetime.now()
        start_time = end_time - timedelta(minutes=time_window_minutes)
        
        df = self.get_movement_data(start_time, end_time)
        
        # Calculate time spent in each zone by employee
        time_spent = df.groupby(['name', 'zone_name']).size().unstack(fill_value=0)
        time_spent = time_spent.div(60)  # Convert to hours
        
        plt.figure(figsize=(12, 6))
        sns.heatmap(time_spent, annot=True, fmt='.2f', cmap='YlOrRd')
        plt.title(f'Time Spent (Hours) by Employee in Each Zone - Last {time_window_minutes} minutes')
        plt.ylabel('Employee Name')
        plt.savefig('time_heatmap.png', bbox_inches='tight', dpi=300)
        plt.close()
    
    def create_zone_heatmap(self, time_window_minutes=60):
        end_time = datetime.now()
        start_time = end_time - timedelta(minutes=time_window_minutes)
        
        df = self.get_movement_data(start_time, end_time)
        
        # Create a grid for the heatmap
        x_grid = np.linspace(0, 50, 50)
        y_grid = np.linspace(0, 30, 30)
        heatmap_data = np.zeros((len(y_grid)-1, len(x_grid)-1))
        
        # Count occurrences in each grid cell
        for _, row in df.iterrows():
            x_idx = np.digitize(row.x_coord, x_grid) - 1
            y_idx = np.digitize(row.y_coord, y_grid) - 1
            if 0 <= x_idx < len(x_grid)-1 and 0 <= y_idx < len(y_grid)-1:
                heatmap_data[y_idx, x_idx] += 1
        
        plt.figure(figsize=(15, 10))
        
        # Plot the heatmap
        plt.imshow(heatmap_data, cmap='YlOrRd', extent=[0, 50, 0, 30], origin='lower', aspect='auto')
        plt.colorbar(label='Number of Occurrences')
        
        # Add zone boundaries and names
        conn = self.connect_db()
        zones_df = pd.read_sql_query("SELECT * FROM zones", conn)
        conn.close()
        
        for _, zone in zones_df.iterrows():
            plt.plot([zone.x_min, zone.x_max, zone.x_max, zone.x_min, zone.x_min],
                    [zone.y_min, zone.y_min, zone.y_max, zone.y_max, zone.y_min],
                    'k-', linewidth=2, alpha=0.5)
            plt.text((zone.x_min + zone.x_max)/2,
                    (zone.y_min + zone.y_max)/2,
                    zone.name,
                    horizontalalignment='center',
                    verticalalignment='center',
                    fontsize=12,
                    fontweight='bold',
                    color='black')
        
        plt.title(f'Zone Activity Heatmap - Last {time_window_minutes} minutes', fontsize=14, pad=20)
        plt.xlabel('Length (meters)', fontsize=12)
        plt.ylabel('Width (meters)', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.3)
        plt.savefig('zone_heatmap.png', bbox_inches='tight', dpi=300)
        plt.close()

if __name__ == "__main__":
    analytics = EmployeeAnalytics()
    
    # Generate store layout with zone names
    analytics.plot_store_layout()
    print("Store layout saved as 'store_layout.png'")
    
    # Generate time heatmap
    analytics.create_time_heatmap()
    print("Time heatmap saved as 'time_heatmap.png'")
    
    # Generate zone activity heatmap
    analytics.create_zone_heatmap()
    print("Zone activity heatmap saved as 'zone_heatmap.png'")
