from fastapi.testclient import TestClient
from src.telemetry_api.api import app

# Create a simulated client that bypasses the network layer
client = TestClient(app)

def test_read_root():
    """Verify the health-check endpoint is online."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "online", "message": "Telemetry API is running."}

def test_get_latest_telemetry_format():
    """Verify the telemetry endpoint returns the correct JSON structure."""
    response = client.get("/api/telemetry/latest?limit=2")
    
    # The request should succeed
    assert response.status_code == 200
    
    data = response.json()
    # The response must contain a 'data' key
    assert "data" in data
    # The length of the returned array should not exceed our limit of 2
    assert len(data["data"]) <= 2

    # If there is data in the database, verify the schema is correct
    if len(data["data"]) > 0:
        first_row = data["data"][0]
        assert "timestamp" in first_row
        assert "potentiometer" in first_row
        assert "photoresistor" in first_row
        # Ensure the hardware values are integers
        assert isinstance(first_row["potentiometer"], int)
        assert isinstance(first_row["photoresistor"], int)