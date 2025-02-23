import re
import os
import json
import matplotlib.pyplot as plt
from datetime import datetime

# File paths
html_file_path = '/Users/kearapolovick/Desktop/Takeout/YouTube and YouTube Music/history/watch-history.html'
json_file_path = '/Users/kearapolovick/Desktop/Takeout/Chrome/History.json'

# Function to extract timestamps from YouTube HTML file
def extract_html_datetimes(file_path):
    if not os.path.exists(file_path):
        print("Error: YouTube file not found. Check the path:", file_path)
        return []
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    datetime_pattern = re.compile(r'([A-Za-z]{3} \d{1,2}, \d{4}, \d{1,2}:\d{2}:\d{2}\s?[AP]M)')
    matches = datetime_pattern.findall(content)
    
    return sorted(datetime.strptime(dt, '%b %d, %Y, %I:%M:%S %p') for dt in matches)

# Function to extract timestamps from Chrome JSON file
def extract_json_datetimes(file_path):
    if not os.path.exists(file_path):
        print("Error: Chrome file not found. Check the path:", file_path)
        return []
    
    with open(file_path, 'r') as file:
        data = json.load(file)

    chrome_history = data.get('Chrome Browser History', [])
    
    timestamps = []
    for entry in chrome_history:
        timestamp = entry.get('time_usec', 0)
        if timestamp:
            timestamps.append(datetime.utcfromtimestamp(timestamp / 1_000_000))
    
    return sorted(timestamps)

# Function to plot inactivity periods
def plot_inactivity_periods(datetimes):
    inactivity_start_hours = []
    inactivity_end_hours = []
    inactivity_lengths = []
    
    for i in range(1, len(datetimes)):
        gap = (datetimes[i] - datetimes[i-1]).total_seconds() / 3600  # Convert gap to hours
        if 5 <= gap <= 12:  # Consider inactivity only if the gap is between 5 and 12 hours
            inactivity_start_hours.append(datetimes[i-1].hour)  # Start of inactivity
            inactivity_end_hours.append(datetimes[i].hour)  # End of inactivity
            inactivity_lengths.append(gap)
    
    plt.figure(figsize=(10, 5))
    
    # Scatter plot: blue for start, pink for end
    plt.scatter(inactivity_start_hours, inactivity_lengths, color='royalblue', alpha=0.7, label="Start of Inactivity")
    plt.scatter(inactivity_end_hours, inactivity_lengths, color='deeppink', alpha=0.7, label="End of Inactivity")

    plt.xlabel("Time of Day")
    plt.ylabel("Length of Inactivity (hours)")
    plt.title("Keara's Periods of Inactivity (5-12 hours)")

    # Convert hours to 12-hour format with AM/PM
    hour_labels = ["12A"] + [f"{h}A" for h in range(1, 12)] + ["12P"] + [f"{h}P" for h in range(1, 12)]
    plt.xticks(range(24), hour_labels, rotation=45, fontsize=8, ha='right')

    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend()
    plt.show()

# Extract timestamps from both sources
html_datetimes = extract_html_datetimes(html_file_path)
json_datetimes = extract_json_datetimes(json_file_path)

# Merge and sort both datasets
all_datetimes = sorted(html_datetimes + json_datetimes)

# Plot inactivity periods
plot_inactivity_periods(all_datetimes)
