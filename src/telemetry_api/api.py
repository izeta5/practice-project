from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

app = FastAPI(title="Hardware Telemetry API")

# Enable CORS for the frontend dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "telemetry.sqlite3"

def get_db_connection():
    # Connect to the database
    conn = sqlite3.connect(DB_PATH)
    # Configure SQLite to return dictionary-like rows instead of bare tuples
    conn.row_factory = sqlite3.Row 
    return conn

@app.get("/")
def read_root():
    return {"status": "online", "message": "Telemetry API is running."}

@app.get("/api/telemetry/latest")
def get_latest_telemetry(limit: int = 10):
    """Fetches the most recent sensor readings."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Query the database, sorting by newest first
        cursor.execute(
            "SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT ?", 
            (limit,)
        )
        rows = cursor.fetchall()
        conn.close()
        
        # Convert the rows into clean JSON
        return {"data": [dict(row) for row in rows]}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))