from pydantic import BaseModel, Field
from typing import List

class HardwarePayload(BaseModel):
    potentiometer: int = Field(ge=0, le=1023, description="Raw 10-bit ADC value")
    photoresistor: int = Field(ge=0, le=1023, description="Raw 10-bit ADC value")

class SensorRow(HardwarePayload):
    id: int
    timestamp: str

class TelemetryResponse(BaseModel):
    data: List[SensorRow]