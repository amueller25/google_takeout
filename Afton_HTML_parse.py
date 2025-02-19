from bs4 import BeautifulSoup
import re
from datetime import datetime
import matplotlib.pyplot as plt
from collections import Counter

# Path to the HTML file
# This is the path for my (Afton's) search-history.html
file_path = r"C:\Users\equus\CS4501\search-history.html"

# Step 1: Read the content of the HTML file
try:
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
        print("HTML content successfully read!")
except FileNotFoundError:
    print(f"File not found at path: {file_path}")
    raise

# Step 2: Parse HTML with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Step 3: Extract relevant time content (ignore date)
hours = []

# Find all divs with the class 'content-cell'
for div in soup.find_all('div', {'class': 'content-cell'}):
    text = div.get_text()
    
    # Search for 'Watched at' or 'Searched for' timestamps in the text
    match = re.search(r'(Watched\s+at|Searched\s+for)[^<]*\s+(\d{1,2}:\d{2}:\d{2}\s*[APM]{2}\s*EST)', text)
    
    if match:
        time_part = match.group(2)  # Extract time part (without date)
        
        # Convert the extracted time part to a datetime object (only the time part)
        try:
            dt = datetime.strptime(time_part, "%I:%M:%S %p EST")
            hours.append(dt.hour)  # Only store the hour part
        except ValueError as e:
            print(f"Error parsing time {time_part}: {e}")

# Debugging: Check how many valid hours were parsed
print(f"Successfully parsed {len(hours)} time entries.")

# Step 4: Count occurrences of each hour (0 to 23)
hour_counts = Counter(hours)
print(f"Hour counts: {hour_counts}")

# Step 5: Plot data if we have valid hours
if hours:
    # Prepare data for plotting
    x = list(range(24))  # All 24 hours of the day
    y = [hour_counts.get(i, 0) for i in x]  # Get count for each hour (default 0 if no activity)

    # Plotting the data
    plt.figure(figsize=(10, 6))
    plt.bar(x, y, color='pink')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Number of Activities')
    plt.title('Afton Mueller:  YouTube Activity by Hour of the Day')
    plt.xticks(x)  # Show all 24 hours
    plt.grid(True)
    plt.tight_layout()  # Ensures labels don't get cut off
    plt.show()
else:
    print("No valid time data to plot!")
