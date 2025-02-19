import matplotlib.pyplot as plt

# Example: Plotting activities over time
# Basic code to plot the parsed data
times = ['2025-02-01 22:00', '2025-02-01 23:00', '2025-02-02 00:00']  # Replace with real times
activities = [1, 0, 1]  # 1 = activity, 0 = no activity (hypothetical)

plt.plot(times, activities)
plt.xlabel('Time')
plt.ylabel('Activity')
plt.title('Activity Over Time')
plt.xticks(rotation=45)
plt.show()

