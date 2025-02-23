import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Path to your JSON file
# This is the path for Afton's chrome json data
file_path = r'C:\Users\equus\CS4501\History.json'

# Function to convert microsecond timestamp to human-readable format
def convert_to_readable_time(microseconds):
    # Convert microseconds to seconds
    timestamp = microseconds / 1_000_000
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

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
plt.hist(df['hour_of_day'], bins=range(24), edgecolor='black', color='pink', alpha=0.7)

# Customize the plot
plt.title('Afton Mueller:  Google Chrome Activity by Hour of the Day')
plt.xlabel('Hour of the Day')
plt.ylabel('Number of Visits')
plt.xticks(range(24))  # Show all hours from 0 to 23
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.tight_layout()

# Show the plot
plt.show()
