import os
import re
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

search_data = "Takeout2/YouTube and YouTube Music/history/search-history.html"
watch_data = "Takeout2/YouTube and YouTube Music/history/watch-history.html"
chrome_data = "Takeout1\Chrome\History.json"

def extract_json_datetimes(file_path):
    if not os.path.exists(file_path):
        print("Error: Chrome file not found. Check the path:", file_path)
        return []
    
    with open(file_path, 'r', encoding="utf-8") as file:
        data = json.load(file)

    chrome_history = data.get('Browser History', [])
    
    timestamps = []
    for entry in chrome_history:
        timestamp = entry.get('time_usec', 0)
        if timestamp:
            timestamps.append(datetime.utcfromtimestamp(timestamp / 1_000_000))
    
    return sorted(timestamps)

def extract_youtube_timestamps(file_path):
    """
    Extracts YouTube watch timestamps from the provided HTML data.
    Returns a list of datetime objects.
    """
    if not os.path.exists(file_path):
        print("Error: YouTube file not found. Check the path:", file_path)
        return []
    
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            html_content = file.read()
            print("HTML content successfully read!")
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return []  # Return an empty DataFrame if the file is missing
    
    soup = BeautifulSoup(html_content, "html.parser")

    # Extract all text content from the HTML
    text_content = soup.get_text(" ", strip=True)  # Join text with spaces to maintain structure
    text_content = text_content.replace("\u202f", " ")  # Replace non-breaking spaces

    # for debugging
    # print("🔍 Sample Extracted Text:", text_content[:500])

    timestamps = []
    
    # Adjusted regex: supports missing commas, varying spaces, and optional seconds
    pattern = re.compile(r"([A-Za-z]+ \d{1,2}, \d{4}, \d{1,2}:\d{2}:\d{2} [APM]{2}) [A-Z]+")

    for match in pattern.findall(text_content):
        full_timestamp = match
        try:
            dt_object = datetime.strptime(full_timestamp, "%b %d, %Y, %I:%M:%S %p")  # Parse with time zone            
            timestamps.append(dt_object)
        except ValueError:
            print(f"❌ Failed to parse: {full_timestamp}")

    return sorted(timestamps)  # Return sorted timestamps

def infer_sleep_periods(timestamps):
    """
    Infers sleep periods by finding large gaps in YouTube activity.
    Returns a list of probable sleep times.
    """
    sleep_data = []
    if not timestamps:
        print("No timestamps available.")
        return sleep_data
    
    # min_sleep_gap = timedelta(hours=4)  # Assume sleep occurs in inactivity gaps > 4 hours

    for i in range(1, len(timestamps)):
        prev, curr = timestamps[i-1], timestamps[i]
        gap = (curr - prev).total_seconds() / 3600  # Convert to hours
        
        # print(f"Checking gap: {gap:.2f} hours between {prev} and {curr}")  # Debugging

        if 4 <= gap <= 14:  # Adjusted sleep gap range
            sleep_start = prev.hour
            wake_time = curr.hour
            sleep_data.append((sleep_start, wake_time))

    return sleep_data

def infer_specific_sleep_periods(timestamps):
    """
    Infers sleep periods by finding large gaps in YouTube activity.
    Returns a list of probable sleep times.
    """
    sleep_data = []
    if not timestamps:
        return sleep_data
    
    daily_gaps = {}
    
    # min_sleep_gap = timedelta(hours=4)  # Assume sleep occurs in inactivity gaps > 4 hours

    for i in range(1, len(timestamps)):
        prev, curr = timestamps[i-1], timestamps[i]
        gap = (curr - prev).total_seconds() / 3600  # Convert to hours
        
        prev_date = prev.date()
        sleep_start_hour, wake_hour = prev.hour, curr.hour

        if prev_date not in daily_gaps or gap > daily_gaps[prev_date][1]:
            # Ensure sleep start is between 8 PM - 5 AM and wake-up is between 5 AM - 2 PM
            if (20 <= sleep_start_hour or sleep_start_hour < 5) and (5 <= wake_hour < 14):
                daily_gaps[prev_date] = (sleep_start_hour, wake_hour)

    return list(daily_gaps.values())

def plot_sleep_patterns(sleep_data):
    if not sleep_data:
        print("No sleep data found.")
        return

    sleep_starts, wake_times = zip(*sleep_data)

    plt.figure(figsize=(12, 5))

    # Define custom hour labels
    hour_labels = ["12A"] + [f"{h}A" for h in range(1, 12)] + ["12P"] + [f"{h}P" for h in range(1, 12)]

    # Sleep Start Histogram
    plt.subplot(1, 2, 1)
    plt.hist(sleep_starts, bins=range(25), color='lightskyblue', edgecolor='royalblue', alpha=0.7, density=True)
    plt.xlabel("Hour of Day (Sleep Start)", fontsize=10)
    plt.ylabel("Frequency (Normalized)", fontsize=10)
    plt.title("Genevieve's Inferred Sleep Start Times (8P - 5A)", fontsize=12)
    plt.xticks(range(24), hour_labels, rotation=45, fontsize=8, ha='right')

    # Wake-up Time Histogram
    plt.subplot(1, 2, 2)
    plt.hist(wake_times, bins=range(25), color='lightpink', edgecolor='deeppink', alpha=0.7, density=True)
    plt.xlabel("Hour of Day (Wake-up Time)", fontsize=10)
    plt.ylabel("Frequency (Normalized)", fontsize=10)
    plt.title("Genevieve's Inferred Wake-up Times (5A - 2P)", fontsize=12)
    plt.xticks(range(24), hour_labels, rotation=45, fontsize=8, ha='right')

    plt.tight_layout()
    plt.show()

# Extract timestamps
search_timestamps = extract_youtube_timestamps(search_data)
watch_timestamps = extract_youtube_timestamps(watch_data)
chrome_timestamps = extract_json_datetimes(chrome_data)

all_timestamps = sorted(search_timestamps + watch_timestamps + chrome_timestamps)
# print(timestamps)

# Filter last 2 months of data
cutoff_date = datetime.now() - timedelta(days=60)
filtered_timestamps = [t for t in all_timestamps if t >= cutoff_date]

# Infer sleep times
sleep_times = infer_specific_sleep_periods(filtered_timestamps)

# Display results
plot_sleep_patterns(sleep_times)