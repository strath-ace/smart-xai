# PEP calculation - 5th file, used to create plot chart.

# This file is used to plot an nxm matrix plot showing where every 2 action can be replaced at every/
# instance throughout a scheduled day displaying where conflicts occur.

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.colors import ListedColormap
from Earth_Observation_Satellite_Case_Study.Argumentation.Abstract_Argumentation.PEP.PEP_1_2_Exchange. \
    PEP_vio_ex_for_plot import vio_check

# Day number used to name file when saved.
day = 3

# Name of file after saved.
filename = '../../PEP_Results/Day/PEP_1_2_Swap/Attack_summary_a' + str(day) + '.txt'

# Load of attacks summary information.
attack_path_0_1 = '../../PEP_Results/Day/PEP_1_2_Swap/Attack_swap_a' + str(day) + '.txt'
attack_coord_0_1 = open(attack_path_0_1, "r")
count_attack_coord_0_1 = 0

# For loop to count the number of lines in file.
for line in attack_coord_0_1:
    if line != "\n":
        count_attack_coord_0_1 += 1
attack_coord_0_1.close()
print(count_attack_coord_0_1)

# Load data line by line.
attack_coord_0_1 = open(attack_path_0_1, "r")
attack_cp_coord_0_1 = attack_coord_0_1.read()
lines_attack_coord_0_1 = attack_cp_coord_0_1.split('\n')

# Load of argumentation summary information created in file "sep_data_sort".
attack_path = '../../SEP_Results/Day/Argumentation' + str(day) + '.txt'
attack_coord = open(attack_path, "r")
count_attack_coord = 0

# For loop to count the number of lines in file.
for line in attack_coord:
    if line != "\n":
        count_attack_coord += 1
attack_coord.close()
print(count_attack_coord)

# Load data line by line.
attack_coord = open(attack_path, "r")
attack_cp_coord = attack_coord.read()
lines_attack_coord = attack_cp_coord.split('\n')

# To initiate the range of data for the plot.
datastart = 1
# dataend = 1604
# dataend = count_attack_coord-2270
dataend = count_attack_coord - 2

# Extract the starting (minimum) time from the generated schedule for 1 day.
min_number = int(lines_attack_coord[datastart].split()[0])

# Extract the last/end time of choice from the generated schedule for 1 day.
max_number = int(lines_attack_coord[dataend].split()[0])

# Test to see the starting and end time of the schedule to ensure data is extracted correctly.
print('min', min_number)
print('max', max_number)

# Create n rows by m columns with starting point for every 5 seconds to the end point.
# Every action requires 5 seconds to complete.
grid_size = 5
x = np.arange(min_number, max_number + 1, grid_size)
y = np.arange(min_number, max_number + 1, grid_size)

# Initiate for data tabulation.
x_coordinates = []
y_coordinates = []

# Extract the actions from the schedule with start and end points and create/
# 2 separate files for grid or matrix.

for i in range(datastart, dataend):
    S_x_data = int(lines_attack_coord[i].split()[4])
    S_y_data = int(lines_attack_coord[i].split()[4])
    x_coordinates.append(S_x_data)
    y_coordinates.append(S_y_data)

# Create a list to collect the summary of attacks.
swap_1_2_summary = []

# Extract the data 'start time', 'swap location', 'memory violation'  collect a summary of the attacks.
for n in range(1, count_attack_coord_0_1):
    # for n in range (9275768-1,9275768+2):
    swap_1_2x = int(lines_attack_coord_0_1[n].split()[1])
    swap_1_2y = int(lines_attack_coord_0_1[n].split()[2])
    # print(n,lines_attack_coord_0_1[n].split())
    swap_1_2_vio = int(lines_attack_coord_0_1[n].split()[10])
    swap_1_2_summary.append([swap_1_2x, swap_1_2y, swap_1_2_vio])

# write data to file.
file1 = open(filename, 'w')
df = pd.DataFrame(swap_1_2_summary)
file1.writelines(df.to_string(header=False, index=False))
# print(len(swap_1_2_summary))


# Create a colormap with two colors, min and max are chosen so that their center is the pivot value.
cmap = ListedColormap(['indigo', 'red', 'gold'])

pivot_value = 1

# Converting the coordinates to arrays.
x_coordinates = np.array(x_coordinates)
y_coordinates = np.array(y_coordinates)

# Create list for plotting grids.
x1_coordinates = []
y1_coordinates = []
vio_list = []

# This function is used to check where every 2 action can be replaced at every instance throughout a scheduled day/
# and display where a violation occurs. The order of the possible exchange of the actions are 0,1; 1,0; 0,2; 2,0; 1,2;/
# 2,1; 0,-1; -1,0; 1,-1; -1,1; 2,-1; -1,2.
# For i in range(len(x) - 2):
for i in range(1603):
    for j in range(len(y) - 2):

        # Re-initiate vio to be 0 as each time the code is executed and a violation of memory occurs, this will/
        # be carried over.
        vio = 0

        # If statement to see if actions overlap containing action 0 and 1.
        if [x_coordinates[i], y_coordinates[j]] == [0, 1]:

            # Returning values from function that checks for violations.
            x1, y1, vio = vio_check(vio, x[i], y[j], swap_1_2_summary)

            if vio == 1:
                x1_coordinates.append(x1)
                y1_coordinates.append(y1)
            else:
                vio = 0

        # If statement to see if actions overlap containing action 1 and 0.
        elif [x_coordinates[i], y_coordinates[j]] == [1, 0]:

            # Returning values from function that checks for violations.
            x1, y1, vio = vio_check(vio, x[i], y[j], swap_1_2_summary)

            if vio == 1:
                x1_coordinates.append(x1)
                y1_coordinates.append(y1)
            else:
                vio = 0

        # If statement to see if actions overlap containing action 0 and 2.
        elif [x_coordinates[i], y_coordinates[j]] == [0, 2]:

            # Returning values from function that checks for violations.
            x1, y1, vio = vio_check(vio, x[i], y[j], swap_1_2_summary)

            if vio == 1:
                x1_coordinates.append(x1)
                y1_coordinates.append(y1)
            else:
                vio = 0

        # If statement to see if actions overlap containing action 2 and 0.
        elif [x_coordinates[i], y_coordinates[j]] == [2, 0]:

            # Returning values from function that checks for violations.
            x1, y1, vio = vio_check(vio, x[i], y[j], swap_1_2_summary)

            if vio == 1:
                x1_coordinates.append(x1)
                y1_coordinates.append(y1)
            else:
                vio = 0

        # If statement to see if actions overlap containing action 1 and 2.
        elif [x_coordinates[i], y_coordinates[j]] == [1, 2]:

            # Returning values from function that checks for violations.
            x1, y1, vio = vio_check(vio, x[i], y[j], swap_1_2_summary)

            if vio == 1:
                x1_coordinates.append(x1)
                y1_coordinates.append(y1)
            else:
                vio = 0

        # If statement to see if actions overlap containing action 2 and 1.
        elif [x_coordinates[i], y_coordinates[j]] == [2, 1]:

            # Returning values from function that checks for violations.
            x1, y1, vio = vio_check(vio, x[i], y[j], swap_1_2_summary)

            if vio == 1:
                x1_coordinates.append(x1)
                y1_coordinates.append(y1)
            else:
                vio = 0

        # If statement to see if actions overlap containing action 0 and -1.
        elif [x_coordinates[i], y_coordinates[j]] == [0, -1]:

            # Returning values from function that checks for violations.
            x1, y1, vio = vio_check(vio, x[i], y[j], swap_1_2_summary)

            if vio == 1:
                x1_coordinates.append(x1)
                y1_coordinates.append(y1)
            else:
                vio = 0

        # If statement to see if actions overlap containing action -1 and 0.
        elif [x_coordinates[i], y_coordinates[j]] == [-1, 0]:

            # Returning values from function that checks for violations.
            x1, y1, vio = vio_check(vio, x[i], y[j], swap_1_2_summary)

            if vio == 1:
                x1_coordinates.append(x1)
                y1_coordinates.append(y1)
            else:
                vio = 0

        # If statement to see if actions overlap containing action 1 and -1.
        elif [x_coordinates[i], y_coordinates[j]] == [1, -1]:

            # Returning values from function that checks for violations.
            x1, y1, vio = vio_check(vio, x[i], y[j], swap_1_2_summary)

            if vio == 1:
                x1_coordinates.append(x1)
                y1_coordinates.append(y1)
            else:
                vio = 0

        # If statement to see if actions overlap containing action -1 and 1.
        elif [x_coordinates[i], y_coordinates[j]] == [-1, 1]:

            # Returning values from function that checks for violations.
            x1, y1, vio = vio_check(vio, x[i], y[j], swap_1_2_summary)

            if vio == 1:
                x1_coordinates.append(x1)
                y1_coordinates.append(y1)
            else:
                vio = 0

        # If statement to see if actions overlap containing action 2 and -1.
        elif [x_coordinates[i], y_coordinates[j]] == [2, -1]:

            # Returning values from function that checks for violations.
            x1, y1, vio = vio_check(vio, x[i], y[j], swap_1_2_summary)

            if vio == 1:
                x1_coordinates.append(x1)
                y1_coordinates.append(y1)
            else:
                vio = 0

        # If statement to see if actions overlap containing action -1 and 2.
        elif [x_coordinates[i], y_coordinates[j]] == [-1, 2]:

            # Returning values from function that checks for violations.
            x1, y1, vio = vio_check(vio, x[i], y[j], swap_1_2_summary)

            if vio == 1:
                x1_coordinates.append(x1)
                y1_coordinates.append(y1)
            else:
                vio = 0

        else:
            x1 = x_coordinates[i]
            y1 = y_coordinates[j]
            vio = 0

        x1_coordinates.append(x1)
        y1_coordinates.append(y1)
        vio_list.append(vio)

# Function to plot figure.
f = plt.figure()
f.set_figwidth(20)
f.set_figheight(30)

# Plot for histogram with colour map.
binvalues, _, _, _ = plt.hist2d(x1_coordinates, y1_coordinates, bins=[x, y], cmap=cmap)

# Conditions to determine the colour of position in the plot where violations occur when 2 actions attack each other.
for i in range(len(x) - 1):
    for j in range(len(y) - 1):
        plt.text((x[i] + x[i + 1]) / 2, (y[j] + y[j + 1]) / 2, [x_coordinates[i], y_coordinates[j]],
                 color='white' if binvalues[i, j] < pivot_value else 'black',
                 ha='center', va='center', size=8)

plt.yticks(y)
plt.xticks(x, rotation=90)
plt.gca().invert_yaxis()
plt.grid(True, ls='-', lw=1, color='black')

plt.show()
