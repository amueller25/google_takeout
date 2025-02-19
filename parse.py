import json
from datetime import datetime

# Load JSON data
# Everyone will have to edit this line to properly point to their file destination
with open('path_to_your_chrome_history.json') as f:
    data = json.load(f)

# Convert timestamps to human-readable format
for entry in data:
    timestamp = entry['time'] / 1000  # Convert milliseconds to seconds
    time = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    print(time)

