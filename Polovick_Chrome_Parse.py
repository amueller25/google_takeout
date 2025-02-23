# #Keara Polovick, PA 1

import matplotlib.pyplot as plt
import json
from datetime import datetime, timedelta

# Function to load data from Google Takeout JSON
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

# Load the data from Google Takeout Chrome history file
file_path = '/Users/kearapolovick/Desktop/Takeout/Chrome/History.json'  # Replace with your actual file path
data = load_chrome_history(file_path)

# Extract time and convert to datetime
timestamps = [convert_usec_to_datetime(entry['time_usec']) for entry in data]
timestamps.sort()
print(timestamps[0])

# Extract only the hour of the day (ignoring the date)
hours = [extract_hour(t) for t in timestamps]

# Create a histogram of browsing activity based on the hour of the day
plt.figure(figsize=(10, 6))
plt.hist(hours, bins=range(25), edgecolor='black', color='pink', alpha=0.7)

# Convert hours to 12-hour format with AM/PM
labels = [f"{(h-1)%12+1}{'A' if h < 12 else 'P'}" for h in range(24)]

# Customize the plot
plt.title("Keara's Google Chrome Activity by Hour of the Day")
plt.xlabel('Time of Day')
plt.ylabel('Number of Visits')

# Update x-axis labels with 12-hour format and slant them
plt.xticks(range(24), labels, rotation=45, ha='right')

plt.grid(True)
plt.tight_layout()  # Ensures labels don't get cut off

# Show the plot
plt.show()
