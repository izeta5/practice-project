import serial
import time
import sys
import sqlite3
from datetime import datetime

PORT = "/dev/cu.usbmodem1201" 
BAUD_RATE = 115200
DB_PATH = "telemetry.sqlite3" # This will save to project root

def init_db():
    """Creates the database and schema if it does not exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            potentiometer INTEGER NOT NULL,
            photoresistor INTEGER NOT NULL
        )
    ''')
    conn.commit()
    return conn

def start_telemetry():
    # Initialize the database connection
    db_conn = init_db()
    cursor = db_conn.cursor()

    try:
        print(f"Connecting to Arduino on {PORT}...")
        board = serial.Serial(PORT, BAUD_RATE, timeout=1)
        time.sleep(2) 
        print("Listening and saving to database... (Press Ctrl+C to stop)")

        while True:
            if board.in_waiting > 0:
                raw_data = board.readline().decode('utf-8').strip()
                
                if raw_data:
                    pot_val, light_val = raw_data.split(',')
                    timestamp = datetime.now().isoformat()
                    
                    # Insert data securely using tuple binding (?)
                    cursor.execute(
                        "INSERT INTO sensor_data (timestamp, potentiometer, photoresistor) VALUES (?, ?, ?)",
                        (timestamp, int(pot_val), int(light_val))
                    )
                    db_conn.commit()
                    
                    print(f"[{timestamp}] Saved -> Pot: {pot_val} | Light: {light_val}")

    except serial.SerialException:
        print(f"Error: Could not connect to {PORT}.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nClosing hardware stream and database safely.")
        board.close()
        db_conn.close()
        sys.exit(0)
    except ValueError:
        pass 

if __name__ == "__main__":
    start_telemetry()