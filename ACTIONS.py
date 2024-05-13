import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import serial
import time

# Load your dataset from CSV file
df = pd.read_csv('FinalData.csv')

# Separate features and target
X = df.drop('Actions', axis=1)
y = df['Actions']

# Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the Random Forest Classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Calculate accuracy on test set
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Function to predict activity given real-time data
def predict_activity(real_time_data):
    try:
        # Convert real-time data to DataFrame
        real_time_df = pd.DataFrame([real_time_data], columns=X.columns)
        # Predict activity
        prediction = clf.predict(real_time_df)
        return prediction[0]
    except Exception as e:
        print("Error predicting activity:", e)
        return None

# Function to take real-time data from the serial port
def get_real_time_data():
    try:
        # Define the COM port and baud rate
        com_port = '/dev/ttyUSB0'
        baud_rate = 9600

        # Open the serial port
        with serial.Serial(com_port, baud_rate) as ser:
            # Read a line of data from the serial port
            line = ser.readline().decode('utf-8').strip()
            
            # Split the received line into flex sensor and MPU6050 values
            data_parts = line.split(',')
            if len(data_parts) == 14:  # Ensure exactly 14 data parts are received
                flex_values = [float(value) for value in data_parts[:10]]
                mpu_values = [float(value) for value in data_parts[10:]]
                real_time_data = dict(zip(X.columns, flex_values + mpu_values))
                return real_time_data
            else:
                print("Error: Incomplete data received from serial port")
                return None
    except serial.SerialException as e:
        print("Error reading real-time data:", e)
        return None

# Mapping of activity names based on activity numbers
actions = {
    1: "All-Ok",
    2: "Namaste",
    3: "Power",
    4: "Thumbs-up",
    5: "Victory",
    6: "Sorry",
    7: "Welcome",
    8: "Call_Me",
    9: "Rock",
    10: "Loser",
}

# Continuous prediction loop
while True:
    real_time_data = get_real_time_data()
    if real_time_data is not None:
        print("Reading data from sensor...")
        predicted_activity_number = predict_activity(real_time_data)
        if predicted_activity_number is not None:
            predicted_activity_name = actions.get(predicted_activity_number, "Unknown")
            print("Predicted Activity Name:", predicted_activity_name)
    #time.sleep(1)  # Add a 1-second delay
