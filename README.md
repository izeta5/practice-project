# Real-Time Hardware Telemetry Pipeline

An end-to-end telemetry ingestion and visualization pipeline that bridges physical microcontrollers with asynchronous web technologies. 

Designed to capture, persist, and serve high-frequency hardware sensor data with zero blocking.

## Architecture Stack
* **Hardware:** Arduino Uno (C++), 10-bit ADC, analog potentiometers and photoresistors.
* **Ingestion Layer:** Python `pyserial` for continuous, high-baud rate serial monitoring.
* **Persistence:** SQLite for localized, timestamped telemetry logging.
* **API Layer:** FastAPI / Uvicorn serving asynchronous REST endpoints.
* **Visualization:** Vanilla JS and Chart.js for zero-compile, real-time frontend polling.

## Data Flow
`Sensors -> USB Serial (115200 baud) -> Python Listener -> SQLite -> FastAPI -> Browser`

## Running the Project locally

### 1. Hardware Setup
Flash the included C++ sketch (`hardware/telemetry.ino`) to your Arduino. Ensure a potentiometer is wired to `A0` and a photoresistor (via 10k voltage divider) to `A5`.

### 2. Environment Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt