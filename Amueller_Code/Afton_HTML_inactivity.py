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

def plot_inactivity_periods(datetimes):
    inactivity_start_hours = []
    inactivity_lengths = []
    
    for i in range(1, len(datetimes)):
        gap = (datetimes[i] - datetimes[i-1]).total_seconds() / 3600  # Convert gap to hours
        if 5 <= gap <= 12:  # Consider inactivity only if the gap is between 5 and 12 hours
            inactivity_start_hours.append(datetimes[i-1].hour)
            inactivity_lengths.append(gap)
    
    plt.figure(figsize=(10, 5))
    plt.scatter(inactivity_start_hours, inactivity_lengths, color='pink', alpha=0.7)
    plt.xlabel("Hour of day (start of inactivity)")
    plt.ylabel("Length of inactivity (hours)")
    plt.title("Periods of Inactivity in YouTube Watch History (5-12 hours)")
    
    # Format x-axis labels as 12A, 1A, ..., 12P, 1P, ..., 11P
    hour_labels = ["12A"] + [f"{h}A" for h in range(1, 12)] + ["12P"] + [f"{h}P" for h in range(1, 12)]
    plt.xticks(range(24), hour_labels)
    
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

# Specify the path to your file
file_path = r"C:\Users\equus\CS4501\watch-history.html"

datetimes = extract_datetimes(file_path)
plot_inactivity_periods(datetimes)
