import re
import os
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

def extract_datetimes(file_path):
    if not os.path.exists(file_path):
        print("Error: File not found. Check the path:", file_path)
        exit()
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Regular expression to find date and time combinations
    datetime_pattern = re.compile(r'([A-Za-z]{3} \d{1,2}, \d{4}, \d{1,2}:\d{2}:\d{2}\s?[AP]M)')
    matches = datetime_pattern.findall(content)
    
    # Convert extracted datetime strings to datetime objects
    datetime_objects = [datetime.strptime(dt, '%b %d, %Y, %I:%M:%S %p') for dt in matches]
    
    return sorted(datetime_objects)

def find_sleep_periods(datetimes):
    sleep_data = []

    if not datetimes:
        return sleep_data

    daily_gaps = {}

    # Identify longest inactivity per day
    for i in range(1, len(datetimes)):
        prev, curr = datetimes[i-1], datetimes[i]
        gap = (curr - prev).total_seconds() / 3600  # Convert to hours
        
        prev_date = prev.date()
        sleep_start_hour, wake_hour = prev.hour, curr.hour
        
        if prev_date not in daily_gaps or gap > daily_gaps[prev_date][1]:
            # Ensure sleep start is between 8 PM (20) - 5 AM (5) and wake-up is between 5 AM (5) - 2 PM (14)
            if (20 <= sleep_start_hour or sleep_start_hour < 5) and (5 <= wake_hour < 14):
                daily_gaps[prev_date] = (sleep_start_hour, wake_hour)

    # Extract sleep start and wake-up times
    sleep_data = list(daily_gaps.values())
    
    return sleep_data

def plot_sleep_patterns(sleep_data):
    if not sleep_data:
        print("No sleep data found.")
        return

    sleep_starts, wake_times = zip(*sleep_data)

    plt.figure(figsize=(12, 5))

    # Sleep Start Histogram
    plt.subplot(1, 2, 1)
    plt.hist(sleep_starts, bins=range(25), color='skyblue', edgecolor='black', alpha=0.7, density=True)
    plt.xlabel("Hour of day (sleep start)")
    plt.ylabel("Frequency (normalized)")
    plt.title("Inferred Sleep Start Times (8 PM - 5 AM)")
    
    # Wake-up Time Histogram
    plt.subplot(1, 2, 2)
    plt.hist(wake_times, bins=range(25), color='lightcoral', edgecolor='black', alpha=0.7, density=True)
    plt.xlabel("Hour of day (wake-up time)")
    plt.ylabel("Frequency (normalized)")
    plt.title("Inferred Wake-up Times (5 AM - 2 PM)")

    # Format x-axis
    hour_labels = ["12A"] + [f"{h}A" for h in range(1, 12)] + ["12P"] + [f"{h}P" for h in range(1, 12)]
    plt.xticks(range(24), hour_labels)

    plt.tight_layout()
    plt.show()

# Specify the path to your file
file_path = r"C:\Users\equus\CS4501\watch-history.html"

datetimes = extract_datetimes(file_path)
sleep_data = find_sleep_periods(datetimes)
plot_sleep_patterns(sleep_data)
