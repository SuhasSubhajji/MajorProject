#include <Wire.h>
#include <SoftwareSerial.h>

const int MPU_ADDRESSES[] = {0x69, 0x68, 0x69, 0x68};
const int flexPins[] = {A0, A1, A2, A3, A4, A5, A6, A7, A8, A9};
const int numFlexSensors = 10;
int flexValues[numFlexSensors]; // Change data type to integer for flex sensor values

const int numMPU = 4;
float gyroMagnitude[numMPU]; // Magnitude of the gyroscope vector for each MPU sensor

SoftwareSerial bluetooth(10, 11); // RX, TX

void setup() {
  Serial.begin(9600); // Initialize serial communication for debugging
  Wire.begin();
  for (int i = 0; i < numMPU; i++) {
    setupMPU(MPU_ADDRESSES[i]);
  }
  
  bluetooth.begin(9600); // Initialize Bluetooth communication
}

void loop() {
  readSensors(); // Read sensor data
  sendSensorData(); // Send sensor data over Bluetooth
  delay(2000); // Delay for stability
}

void setupMPU(const int MPU) {
  Wire.beginTransmission(MPU);
  Wire.write(0x6B);
  Wire.write(0b00000000);
  Wire.endTransmission();

  Wire.beginTransmission(MPU);
  Wire.write(0x1B);
  Wire.write(0b00000000);
  Wire.endTransmission();

  Wire.beginTransmission(MPU);
  Wire.write(0x1C);
  Wire.write(0b00000000);
  Wire.endTransmission();
}

void readSensors() {
  // Read flex sensor data as integers
  for (int i = 0; i < numFlexSensors; i++) {
    int sensorValue = analogRead(flexPins[i]);
    flexValues[i] = sensorValue;
  }

  // Read gyroscope data for each MPU
  for (int i = 0; i < numMPU; i++) {
    getGyroValue(MPU_ADDRESSES[i], i);
  }
}

void getGyroValue(const int MPU, int index) {
  // Start reading from the gyroscope registers (0x43 for X-axis gyro data)
  Wire.beginTransmission(MPU);
  Wire.write(0x43);
  Wire.endTransmission();
  
  // Request 6 bytes of data (2 bytes for each axis - X, Y, and Z)
  Wire.requestFrom(MPU, 6);
  while (Wire.available() < 6);
  
  // Read the gyroscope data
  int16_t gyroX_raw = (Wire.read() << 8 | Wire.read());
  int16_t gyroY_raw = (Wire.read() << 8 | Wire.read());
  int16_t gyroZ_raw = (Wire.read() << 8 | Wire.read());

  // Convert raw data to degrees per second
  float gyroX = gyroX_raw / 131.0;
  float gyroY = gyroY_raw / 131.0;
  float gyroZ = gyroZ_raw / 131.0;

  // Calculate the magnitude of the gyroscope vector
  gyroMagnitude[index] = sqrt(gyroX * gyroX + gyroY * gyroY + gyroZ * gyroZ);
}

void sendSensorData() {
  // Send flex sensor data as integers separated by commas
  for (int i = 0; i < numFlexSensors; i++) {
    bluetooth.print(flexValues[i]);
    if (i < numFlexSensors - 1) {
      bluetooth.print(",");
    }
  }
  bluetooth.print(", "); // Separate flex and MPU data
  
  // Send gyro magnitude data for each MPU separated by commas
  for (int i = 0; i < numMPU; i++) {
    bluetooth.print(gyroMagnitude[i]);
    if (i < numMPU - 1) {
      bluetooth.print(",");
    }
  }
  bluetooth.println(); // End of data
}
