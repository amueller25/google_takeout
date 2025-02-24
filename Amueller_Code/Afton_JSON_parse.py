import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Path to your JSON file
file_path = '/Users/kearapolovick/Desktop/Takeout/Chrome/History.json'

# Function to convert microsecond timestamp to human-readable format
def convert_to_readable_time(microseconds):
    # Convert microseconds to seconds
    timestamp1 = microseconds / 1_000_000
    return datetime.utcfromtimestamp(timestamp1).strftime('%Y-%m-%d %H:%M:%S')

# Load the JSON data
with open(file_path, 'r') as file:
    data = json.load(file)

# Extract 'Chrome Browser History' data
chrome_history = data.get('Chrome Browser History', [])

# Prepare a list to store the parsed data
parsed_data = []

# Process each entry in the Chrome browser history
for entry in chrome_history:
    title = entry.get('title', '')
    url = entry.get('url', '')
    timestamp = entry.get('time_usec', 0)
    
    if timestamp:
        readable_time = convert_to_readable_time(timestamp)
        parsed_data.append({
            'title': title,
            'url': url,
            'timestamp': readable_time
        })

# Create a DataFrame from the parsed data
df = pd.DataFrame(parsed_data)

# Convert the 'timestamp' column to datetime type
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Print the date range (min and max timestamps)
date_range = (df['timestamp'].min(), df['timestamp'].max())
print(f"Date range of data: {date_range[0].strftime('%Y-%m-%d %H:%M:%S')} to {date_range[1].strftime('%Y-%m-%d %H:%M:%S')}")

# Extract the hour of the day (from 0 to 23) from the 'timestamp'
df['hour_of_day'] = df['timestamp'].dt.hour

# Create a histogram of browsing activity based on the hour of the day
plt.figure(figsize=(10, 6))
plt.hist(df['hour_of_day'], bins=range(25), edgecolor='black', color='pink', alpha=0.7)

# Convert hours to 12-hour format with AM/PM
labels = [f"{(h-1)%12+1}{'A' if h < 12 else 'P'}" for h in range(24)]

# Customize the plot
plt.title("Afton's Google Chrome Activity by Hour of the Day")
plt.xlabel('Time of Day')
plt.ylabel('Number of Visits')

# Update x-axis labels with 12-hour format and slant them
plt.xticks(range(24), labels, rotation=45, ha='right')

plt.grid(True)
plt.tight_layout()  # Ensures labels don't get cut off

# Show the plot
plt.show()
