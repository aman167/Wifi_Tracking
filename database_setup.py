
import sqlite3
import pandas as pd

def create_database():
    conn = sqlite3.connect('retail_tracking.db')
    cursor = conn.cursor()
    
    # Create employees table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            employee_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            role TEXT,
            device_mac TEXT UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create zones table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS zones (
            zone_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            x_min REAL,
            x_max REAL,
            y_min REAL,
            y_max REAL
        )
    """)
    
    # Create movement_logs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movement_logs (
            log_id INTEGER PRIMARY KEY,
            employee_id INTEGER,
            timestamp TIMESTAMP,
            x_coord REAL,
            y_coord REAL,
            zone_id INTEGER,
            FOREIGN KEY (employee_id) REFERENCES employees (employee_id),
            FOREIGN KEY (zone_id) REFERENCES zones (zone_id)
        )
    """)
    
    # Create indexes
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_movement_timestamp ON movement_logs(timestamp)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_movement_employee ON movement_logs(employee_id)')
    
    conn.commit()
    return conn

def insert_initial_data(conn):
    cursor = conn.cursor()
    
    # Insert sample zones
    zones = [
        (1, 'Electronics', 0, 15, 0, 15),
        (2, 'Clothing', 15, 30, 0, 15),
        (3, 'Home Goods', 30, 50, 0, 15),
        (4, 'Grocery', 0, 25, 15, 30),
        (5, 'Customer Service', 25, 50, 15, 30)
    ]
    
    cursor.executemany('INSERT OR REPLACE INTO zones (zone_id, name, x_min, x_max, y_min, y_max) VALUES (?, ?, ?, ?, ?, ?)', zones)
    
    # Insert sample employees
    employees = [
        (1, 'John Doe', 'Sales Associate', 'AA:BB:CC:DD:EE:01'),
        (2, 'Jane Smith', 'Cashier', 'AA:BB:CC:DD:EE:02'),
        (3, 'Bob Wilson', 'Stock Clerk', 'AA:BB:CC:DD:EE:03'),
        (4, 'Alice Brown', 'Department Manager', 'AA:BB:CC:DD:EE:04'),
        (5, 'Charlie Davis', 'Sales Associate', 'AA:BB:CC:DD:EE:05')
    ]
    
    cursor.executemany('INSERT OR REPLACE INTO employees (employee_id, name, role, device_mac) VALUES (?, ?, ?, ?)', employees)
    conn.commit()

if __name__ == "__main__":
    conn = create_database()
    insert_initial_data(conn)
    print("Database created and initialized successfully")
    conn.close()
