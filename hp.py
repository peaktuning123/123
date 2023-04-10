import urllib.request
import re
import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns

# Set plot style
sns.set_style('darkgrid')
sns.set_palette('deep')


# Get car name
vehicle_name = input("Enter the name of the vehicle: ")

# Get the URL from the user
url = input("Enter URL: ")

# Make a request to the URL and get the response
request = urllib.request.Request(
    url=url, 
    headers={'User-Agent': 'Mozilla/5.0'}
)
response = urllib.request.urlopen(request).read().decode("utf-8")

# Get the engine speed data
engine_speed_data = re.search(r'name: "Engine speed".*?data:\s*(\[\[.*?\]\])', response, re.DOTALL)
engine_speed_data = engine_speed_data.group(1) if engine_speed_data else ''

# Get the engine torque data
engine_torque_data = re.search(r'name: "Engine torque".*?data:\s*(\[\[.*?\]\])', response, re.DOTALL)
engine_torque_data = engine_torque_data.group(1) if engine_torque_data else ''

# Filter the data
engine_speed_results = []
engine_torque_results = []
for data in [engine_speed_data, engine_torque_data]:
    pattern = r'\[\d+,\s*([\d.]+)\]'
    result = re.findall(pattern, data)
    for i in range(len(result)):
        if i < len(result)-20 and (i < 3 or result[i] != '0.00'):
            if data == engine_speed_data:
                engine_speed_results.append("{:.2f}".format(float(result[i])))
            else:
                engine_torque_results.append("{:.2f}".format(float(result[i])))

# Save the filtered data to files
with open('RPM.txt', 'w') as f:
    f.write('\n'.join(engine_speed_results))

with open('NMOriginal.txt', 'w') as f:
    f.write('\n'.join(engine_torque_results))

with open('NMConverted.txt', 'w') as f:
    f.write('\n'.join(engine_torque_results))

# Read data from RPM.txt
with open('RPM.txt', 'r') as rpm_file:
    rpm_data = rpm_file.readlines()
    lowest_rpm = math.floor(float(rpm_data[0].strip()) / 1000) * 1000
    highest_rpm = math.ceil(float(rpm_data[-1].strip()) / 1000) * 1000

# Read data from NMConverted.txt and convert to lb.in
with open('NMConverted.txt', 'r') as nm_file:
    nm_data_converted = nm_file.readlines()
    nm_data_converted = [float(nm.strip()) / 1.356 for nm in nm_data_converted]

# Read data from NMOriginal
with open('NMOriginal.txt', 'r') as nm_file:
    nm_data_original = nm_file.readlines()
    nm_data_original = [float(nm.strip()) for nm in nm_data_original]

# Calculate horsepower for each line of RPM and NM
hp_data = []
for i in range(min(len(rpm_data), len(nm_data_converted))):
    hp = (nm_data_converted[i] * float(rpm_data[i].strip())) / 5252
    hp_data.append(hp)

# Create the plot
fig, ax = plt.subplots()
ax.plot(nm_data_original, 'b', label='Moment')  # display original data
ax.plot(hp_data, 'r', label='Hestekræfter')

# Set x-axis labels
xtick_positions = range(0, len(rpm_data), len(rpm_data) // len(rpm_data))
xtick_labels = [str(i + 1) for i in range(len(rpm_data))]
ax.grid(alpha=0.3, linestyle='--')
        


# Find highest horsepower and NM values
highest_hp = max(hp_data)
highest_nm = max(nm_data_original)

# Find index of highest horsepower and NM values
index_of_highest_hp = hp_data.index(highest_hp)
index_of_highest_nm = nm_data_original.index(highest_nm)

# Plot highest horsepower and NM points and labels
ax.plot(index_of_highest_nm, highest_nm, 'bo')
ax.annotate(f"{highest_nm:.2f} NM", (index_of_highest_nm, highest_nm), xytext=(index_of_highest_nm, highest_nm+4), ha='center', fontsize=12)
ax.plot(index_of_highest_hp, highest_hp, 'ro')
ax.annotate(f"{highest_hp:.2f} HP", (index_of_highest_hp, highest_hp), xytext=(index_of_highest_hp, highest_hp+4), ha='center', fontsize=12)

# Add labels and legend
ax.set_xlabel('Data')
ax.set_ylabel('Hestekræfter')
ax.legend()

# Add title
ax.text(0.5, 1.05, vehicle_name, ha='center', va='center', transform=ax.transAxes, fontsize=16)

# Add image between title and graph
img = mpimg.imread('peaktuning.png')
ax_image = fig.add_axes([0.4, 0.06, 0.2, 0.2])
ax_image.imshow(img)
ax_image.axis('off')

# Show the plot
plt.show()

# Exit message
print("Færdig!")
