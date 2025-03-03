import re
import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

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

# Function to determine sleep periods from combined data
def find_sleep_periods(datetimes):
    sleep_data = []
    if not datetimes:
        return sleep_data

    daily_gaps = {}

    for i in range(1, len(datetimes)):
        prev, curr = datetimes[i-1], datetimes[i]
        gap = (curr - prev).total_seconds() / 3600  # Convert to hours
        
        prev_date = prev.date()
        sleep_start_hour, wake_hour = prev.hour, curr.hour
        
        if prev_date not in daily_gaps or gap > daily_gaps[prev_date][1]:
            # Ensure sleep start is between 8 PM - 5 AM and wake-up is between 5 AM - 2 PM
            if (20 <= sleep_start_hour or sleep_start_hour < 5) and (5 <= wake_hour < 14):
                daily_gaps[prev_date] = (sleep_start_hour, wake_hour)

    return list(daily_gaps.values())

# Function to plot sleep patterns
def plot_sleep_patterns(sleep_data):
    if not sleep_data:
        print("No sleep data found.")
        return

    sleep_starts, wake_times = zip(*sleep_data)

    plt.figure(figsize=(12, 5))
    hour_labels = ["12A"] + [f"{h}A" for h in range(1, 12)] + ["12P"] + [f"{h}P" for h in range(1, 12)]
    
    plt.subplot(1, 2, 1)
    plt.hist(sleep_starts, bins=range(25), color='lightskyblue', edgecolor='royalblue', alpha=0.7, density=True)
    plt.xlabel("Hour of Day (Sleep Start)", fontsize=10)
    plt.ylabel("Frequency (Normalized)", fontsize=10)
    plt.title("Keara's Inferred Sleep Start Times (8P - 5A)", fontsize=12)
    plt.xticks(range(24), hour_labels, rotation=45, fontsize=8, ha='right')
    plt.axvline(np.mean(sleep_starts), color='red', linestyle='dashed', linewidth=1, label=f"Mean: {np.mean(sleep_starts):.2f}")
    plt.axvline(np.median(sleep_starts), color='blue', linestyle='dashed', linewidth=1, label=f"Median: {np.median(sleep_starts):.2f}")
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.hist(wake_times, bins=range(25), color='lightpink', edgecolor='deeppink', alpha=0.7, density=True)
    plt.xlabel("Hour of Day (Wake-up Time)", fontsize=10)
    plt.ylabel("Frequency (Normalized)", fontsize=10)
    plt.title("Keara's Inferred Wake-up Times (5A - 2P)", fontsize=12)
    plt.xticks(range(24), hour_labels, rotation=45, fontsize=8, ha='right')
    plt.axvline(np.mean(wake_times), color='red', linestyle='dashed', linewidth=1, label=f"Mean: {np.mean(wake_times):.2f}")
    plt.axvline(np.median(wake_times), color='blue', linestyle='dashed', linewidth=1, label=f"Median: {np.median(wake_times):.2f}")
    plt.legend()
    
    plt.tight_layout()
    plt.show()

# Extract timestamps from both sources
html_datetimes = extract_html_datetimes(html_file_path)
json_datetimes = extract_json_datetimes(json_file_path)

# Merge and sort both datasets
all_datetimes = sorted(html_datetimes + json_datetimes)

# Find sleep periods
sleep_data = find_sleep_periods(all_datetimes)

# Plot results
plot_sleep_patterns(sleep_data)
