# #Keara Polovick, PA 1

import matplotlib.pyplot as plt
import json
from datetime import datetime, timedelta

# Function to load data from Google Takeout JSON (replace with actual file path)
def load_chrome_history(file_path):
    with open(file_path) as f:
        data = json.load(f)
    return data["Browser History"]

# Function to convert time_usec (microseconds since epoch) to datetime
def convert_usec_to_datetime(time_usec):
    timestamp_seconds = time_usec / 1_000_000  # Convert microseconds to seconds
    epoch = datetime(1970, 1, 1)
    dt_object = epoch + timedelta(seconds=timestamp_seconds)
    return dt_object

# Function to extract the hour from a datetime object
def extract_hour(dt):
    return dt.hour  # Extract only the hour

# Load the data from your Google Takeout Chrome history file
file_path = '/Users/kearapolovick/Desktop/Takeout/Chrome/History.json'  # Replace with your actual file path
data = load_chrome_history(file_path)

# Extract time and convert to datetime
timestamps = [convert_usec_to_datetime(entry['time_usec']) for entry in data]

# Extract only the hour of the day (ignoring the date)
hours = [extract_hour(t) for t in timestamps]

# Plotting the histogram of activities over hours
plt.figure(figsize=(10, 6))
plt.hist(hours, bins=24, range=(0, 24), color='b', edgecolor='black', alpha=0.7)

# Add titles and labels
plt.title('Keara Polovick: Google Chrome Activity By Hour of the Day')
plt.xlabel('Hour of the Day')
plt.ylabel('Number of Activities')
plt.xticks(range(24))  # Show all 24 hours of the day
plt.grid(True)

# Show the plot
plt.tight_layout()
plt.show()
