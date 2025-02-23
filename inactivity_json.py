import json
import pandas as pd
import datetime
import matplotlib.pyplot as plt

# Path to Google Chrome history JSON file
chrome_history_path = "/Users/kearapolovick/Desktop/Takeout/Chrome/History.json"
# chrome_history_path = r"\Users\equus\CS4501\History.json"

# Step 1: Load JSON data
try:
    with open(chrome_history_path, "r", encoding="utf-8") as file:
        chrome_data = json.load(file)
        print("Chrome history successfully loaded!")
except FileNotFoundError:
    print(f"File not found at path: {chrome_history_path}")
    raise

# Step 2: Extract timestamps
timestamps = []

for entry in chrome_data.get("Browser History", []):  # Ensure we access the right key
    timestamp_usec = entry.get("time_usec")  # Extract timestamp in microseconds
    if timestamp_usec:
        dt = datetime.datetime.utcfromtimestamp(timestamp_usec / 1e6)  # Convert to seconds
        timestamps.append(dt)

# Debugging: Check how many timestamps were parsed
print(f"Successfully parsed {len(timestamps)} timestamps.")

# Step 3: Sort timestamps
timestamps.sort()

# Step 4: Detect inactivity periods
inactivity_threshold_lowerbound = datetime.timedelta(hours=5)  # Define inactivity as 5+ hours, lower bound of sleep time
inactivity_threshold_upperbound = datetime.timedelta(hours=12) # Upper bound of estimated sleep time
sleep_periods = []

for i in range(1, len(timestamps)):
    gap = timestamps[i] - timestamps[i - 1]
    if inactivity_threshold_lowerbound <= gap <= inactivity_threshold_upperbound:
        sleep_periods.append((timestamps[i - 1], timestamps[i], gap))

# Debugging: Print detected inactivity periods
print(f"Detected {len(sleep_periods)} periods of inactivity (sleep).")
for start, end, gap in sleep_periods:
    print(f"🛏️ Inactivity from {start.strftime('%Y-%m-%d %I:%M %p')} to {end.strftime('%I:%M %p')} ({gap} gap)")

# Step 5: Visualizing Inactivity Periods
if sleep_periods:
    sleep_durations = [gap.total_seconds() / 3600 for _, _, gap in sleep_periods]
    # print(sleep_durations)
    start_times = [start.hour for start, _, _ in sleep_periods]

    plt.figure(figsize=(10, 6))
    plt.scatter(start_times, sleep_durations, color='red', alpha=0.6)
    plt.xlabel("Hour of Day (Start of Inactivity)")
    plt.ylabel("Inactivity Duration (Hours)")
    plt.title("Detected Periods of Inactivity (Potential Sleep) - Chrome History")
    plt.xticks(range(24))  # Show all 24 hours
    plt.grid(True)
    plt.tight_layout()
    plt.show()
else:
    print("No significant inactivity periods detected.")
