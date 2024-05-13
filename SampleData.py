import serial
import csv

# Define the COM port
COM_PORT = '/dev/ttyUSB0'
# Define the baudrate
BAUD_RATE = 9600
# Define the number of samples to be saved
NUM_SAMPLES = 30  # Adjust this as per your requirement
# Define the file name
CSV_FILE = 'Loser.csv'

# Create a serial object
ser = serial.Serial(COM_PORT, BAUD_RATE)

# Create a CSV file and write the header
with open(CSV_FILE, mode='w', newline='') as file:
    writer = csv.writer(file)
    header = ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'MPU 1', 'MPU 2', 'MPU 3', 'MPU 4']
    writer.writerow(header)

count = 0
with open(CSV_FILE, mode='a', newline='') as file:
    writer = csv.writer(file)
    while count < NUM_SAMPLES:
        # Read a line of data from the serial port
        data = ser.readline().decode().strip()
        # Split the received data into individual values
        values = data.split(',')
        # Extract flex sensor values
        flex_values = values[:10]
        # Extract MPU sensor values
        mpu_values = values[10:]
        # Write the data to the CSV file
        writer.writerow(flex_values + mpu_values)
        # Print the collected data
        print(f"Sample {count + 1}: {flex_values + mpu_values}")
        # Increment the sample count
        count += 1

# Close the serial port when the program is terminated
ser.close()
