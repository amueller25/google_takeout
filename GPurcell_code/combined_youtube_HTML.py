from bs4 import BeautifulSoup
import re
import pandas as pd
from datetime import datetime
from collections import Counter
import matplotlib.pyplot as plt

# Paths to YouTube search and watch history HTML files
watch_history_path = "Takeout2/YouTube and YouTube Music/history/watch-history.html"
search_history_path = "Takeout2/YouTube and YouTube Music/history/search-history.html"

# Function to parse YouTube HTML files (works for both watch and search history)
def parse_youtube_html(file_path, activity_type):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            html_content = file.read()
            print("HTML content successfully read!")
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return pd.DataFrame()  # Return an empty DataFrame if the file is missing
    
    
    soup = BeautifulSoup(html_content, "html.parser")

    history = []
    hours = []
    
    # Find all activity entries
    for div in soup.find_all('div', {'class': 'content-cell'}):
        text = div.get_text()

        # Extract timestamps from "Watched at" or "Searched for"
        match = re.search(r'(Watched\s+at|Searched\s+for)[^<]*\s+(\d{1,2}:\d{2}:\d{2}\s*[APM]{2}\s*EST)', text)
        if match:
            time_part = match.group(2)  # Extract timestamp

            try:
                # print(f"Extracted timestamp: '{time_part}'")
                dt = datetime.strptime(time_part, "%I:%M:%S %p EST")
                history.append({"title": text.split("\n")[0], "datetime": time_part, "activity": activity_type})
                hours.append(dt.hour)
            except ValueError as e:
                print(f"❌ Error parsing time {time_part}: {e}")
    return hours
    # return pd.DataFrame(history, columns=["title", "datetime", "activity"])

# Parse both watch and search history
watch_df = parse_youtube_html(watch_history_path, "Watch")
search_df = parse_youtube_html(search_history_path, "Search")

# Combine both datasets
youtube_df = watch_df + search_df

hour_counts = Counter(youtube_df)
print(f"Hour counts: {hour_counts}")

# Step 5: Plot data if we have valid hours
if youtube_df:
    # Prepare data for plotting
    x = list(range(24))  # All 24 hours of the day
    y = [hour_counts.get(i, 0) for i in x]  # Get count for each hour (default 0 if no activity)

    # Convert hours to 12-hour format with AM/PM
    labels = [f"{(h-1)%12+1}{'A' if h < 12 else 'P'}" for h in x]

    # Plotting the data
    plt.figure(figsize=(10, 6))
    plt.bar(x, y, color='pink')
    plt.xlabel('Time of Day')
    plt.ylabel('Number of Activities')
    plt.title("Genevieve's YouTube Activity by Hour of the Day")

    # Update x-axis labels with 12-hour format and slant them
    plt.xticks(x, labels, rotation=45, ha='right')

    plt.grid(True)
    plt.tight_layout()  # Ensures labels don't get cut off
    plt.show()
else:
    print("No valid time data to plot!")

# Sort by datetime
# youtube_df.sort_values("datetime", inplace=True)
# print(youtube_df.head(20))
# Save to CSV
# youtube_df.to_csv("combined_youtube_history.csv", index=False)

print("✅ Successfully combined YouTube history (Watch + Search)!")