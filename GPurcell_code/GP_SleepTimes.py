import re
import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# File paths
youtube_csv_path = "combined_youtube_history.csv"
json_file_path = "Takeout1\Chrome\History.json"

# Function to extract timestamps from YouTube csv file
def extract_youtube_datetimes(file_path):
    if not os.path.exists(file_path):
        print("Error: YouTube file not found. Check the path:", file_path)
        return []
    
    # Load CSV
    df = pd.read_csv(file_path)

    # Ensure datetime column exists
    if "datetime" not in df.columns:
        print("❌ Error: 'datetime' column missing in YouTube CSV.")
        return []
    
    # Convert to datetime format
    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")

    # Drop invalid timestamps (NaT values)
    df = df.dropna(subset=["datetime"])
    
    return sorted(df["datetime"].tolist())

# Function to extract timestamps from Chrome JSON file
def extract_json_datetimes(file_path):
    if not os.path.exists(file_path):
        print("Error: Chrome file not found. Check the path:", file_path)
        return []
    
    with open(file_path, 'r', encoding="utf-8") as file:
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

# Extract timestamps from both sources
html_datetimes = extract_youtube_datetimes(youtube_csv_path)
json_datetimes = extract_json_datetimes(json_file_path)

# Merge and sort both datasets
all_datetimes = sorted(html_datetimes + json_datetimes)

# Find sleep periods
sleep_data = find_sleep_periods(all_datetimes)

# Plot results
plot_sleep_patterns(sleep_data)
