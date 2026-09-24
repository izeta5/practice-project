void setup() {
  // Initialize serial communication at 115200 baud for high-speed telemetry
  Serial.begin(115200);
}

void loop() {
  // Read the raw 10-bit ADC values (0-1023)
  int potValue = analogRead(A0);
  int lightValue = analogRead(A5);

  // Print as a clean, comma-separated string for easy Python parsing
  Serial.print(potValue);
  Serial.print(",");
  Serial.println(lightValue);

  // 50ms delay yields a stable 20Hz data stream
  delay(50);
}