import serial
import time
import sys
import sqlite3
from datetime import datetime
from pydantic import ValidationError
from src.telemetry_api.models import HardwarePayload

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
                    try:
                        # 1. Attempt to split the string
                        pot_val, light_val = raw_data.split(',')
                        
                        # 2. Force through Pydantic (Throws ValidationError if not 0-1023 ints)
                        payload = HardwarePayload(potentiometer=int(pot_val), photoresistor=int(light_val))
                        
                        # 3. Save to database only if validation succeeds
                        timestamp = datetime.now().isoformat()
                        cursor.execute(
                            "INSERT INTO sensor_data (timestamp, potentiometer, photoresistor) VALUES (?, ?, ?)",
                            (timestamp, payload.potentiometer, payload.photoresistor)
                        )
                        db_conn.commit()
                        print(f"[{timestamp}] Saved -> Pot: {payload.potentiometer} | Light: {payload.photoresistor}")
                        
                    except (ValueError, ValidationError) as e:
                        # Silently drop the bad frame to keep the pipeline alive
                        print(f"Dropped corrupted hardware frame: {raw_data}")
                        pass

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