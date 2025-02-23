from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd

# Path to YouTube search history HTML
file_path = "/Users/kearapolovick/Desktop/Takeout/YouTube and YouTube Music/history/watch-history.html"

# Path to Afton's Youtube search history HTML
# file_path = r"C:\Users\equus\CS4501\search-history.html"

# Step 1: Read the HTML content
try:
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
        print("HTML content successfully read!")
except FileNotFoundError:
    print(f"File not found at path: {file_path}")
    raise

# Step 2: Parse HTML with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Step 3: Extract timestamps
timestamps = []

for div in soup.find_all('div', {'class': 'content-cell'}):
    text = div.get_text()
    
    # Search for 'Watched at' or 'Searched for' timestamps in the text
    match = re.search(r'(Watched\s+at|Searched\s+for)[^<]*\s+(\d{1,2}:\d{2}:\d{2}\s*[APM]{2}\s*EST)', text)
    
    if match:
        time_part = match.group(2)  # Extract time part (without date)
        
        try:
            dt = datetime.strptime(time_part, "%I:%M:%S %p EST")
            timestamps.append(dt)
        except ValueError as e:
            print(f"Error parsing time {time_part}: {e}")

# Debugging: Check number of valid timestamps
print(f"Successfully parsed {len(timestamps)} timestamps.")

# Step 4: Sort timestamps
timestamps.sort()

# Step 5: Detect inactivity periods
inactivity_threshold_lowerbound = timedelta(hours=5)  # Define inactivity as 5+ hours
inactivity_threshold_upperbound = timedelta(hours=10) # Upper bound of sleep
sleep_periods = []

for i in range(1, len(timestamps)):
    gap = timestamps[i] - timestamps[i - 1]
    if gap >= inactivity_threshold_lowerbound:
        sleep_periods.append((timestamps[i - 1], timestamps[i], gap))

# Debugging: Print detected inactivity periods
print(f"Detected {len(sleep_periods)} periods of inactivity (sleep).")
for start, end, gap in sleep_periods:
    print(f"🛏️ Inactivity from {start.strftime('%I:%M %p')} to {end.strftime('%I:%M %p')} ({gap} gap)")

# Step 6: Visualizing Inactivity Periods
if sleep_periods:
    sleep_durations = [gap.total_seconds() / 3600 for _, _, gap in sleep_periods]
    start_times = [start.hour for start, _, _ in sleep_periods]

    plt.figure(figsize=(10, 6))
    plt.scatter(start_times, sleep_durations, color='blue', alpha=0.6)
    plt.xlabel("Hour of Day (Start of Inactivity)")
    plt.ylabel("Inactivity Duration (Hours)")
    plt.title("Detected Periods of Inactivity (Potential Sleep)")
    plt.xticks(range(24))  # Show all 24 hours
    plt.grid(True)
    plt.tight_layout()
    plt.show()
else:
    print("No significant inactivity periods detected.")
