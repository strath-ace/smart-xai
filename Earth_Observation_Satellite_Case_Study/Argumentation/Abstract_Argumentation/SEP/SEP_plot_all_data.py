# ------------------ Copyright (C) 2022 University of Strathclyde and Author ---------------------------------
# --------------------------------- Author: Cheyenne Powell -------------------------------------------------
# ------------------------- e-mail: cheyenne.powell@strath.ac.uk --------------------------------------------

# This file is used to plot where the breach of attack of action a1 at time 't' with the combined plots of\
# number of images in memory for other actions at any point in time.
# ===========================================================================================================
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
from matplotlib.dates import DateFormatter


day = 3

line_file= '../SEP_Results/Day/line_argument_all_data' + str(day) + '.png'

# load a1 attack file
action_a1_path = '../SEP_Results/Day/Attack_violation_summary_a12' + str(day) + '.txt'
action_a1_coord = open(action_a1_path, "r")
count_a1_coord = 0
# for loop to count the number of lines in file
for line in action_a1_coord:
    if line != "\n":
        count_a1_coord += 1
action_a1_coord.close()
print(count_a1_coord)
# load data line by line
action_a1_coord = open(action_a1_path, "r")
content_a1_coord = action_a1_coord.read()
lines_a1_coord = content_a1_coord.split('\n')

time_interval = 5
# onboard memory is 80% of total memory 2TB - 1,920,000
onboard_mem = int(0.8 * 24 * 10 ** 5)
#  memory required per image
image_mem = 2688
# downlink data rate
downlink_data_rate = 280 * 2 * time_interval
# 5000Kbit/s to process images
process_im_mem = 50 * time_interval


a1_attack = []
for i in range(1, 17278):
    a1_data = lines_a1_coord[i].split()

    start_time = int(a1_data[1])
    end_time = start_time + 5
    time_start_2 = a1_data[7]
    memory =a1_data[8]
    if a1_data[3] == '-' and a1_data[6] == 'Exceeded':
        Status = 'a1_Infeasible'
    elif a1_data[3] == '-' and a1_data[6] == 'Not_exceeded':
        Status = 'a1_Feasible'
    else:
        Status = 'a1_no_attack'

    a1_attack.append([(dt.timedelta(seconds=(int(start_time)))), (dt.timedelta(seconds=(int(end_time)))), Status, (dt.timedelta(seconds=(int(time_start_2)))),memory ])


cp_path = '../SEP_Results/Day/Optimized_Results' + str(day) + '.txt'
cp_coord = open(cp_path, "r")
cp_count_coord = 0
for line in cp_coord:
    if line != "\n":
        cp_count_coord += 1
cp_coord.close()

daily_cp_coord = open(cp_path, "r")
# print(line_count)
cp_count_coord = cp_count_coord
content_cp_coord = daily_cp_coord.read()
lines_cp_coord = content_cp_coord.split('\n')

constraint_land_list=[]

for i in range(1, 17278):
    daily_cp_details = lines_cp_coord[i].split()


    if daily_cp_details[2]  == '0' and daily_cp_details[15] == 'YES':
        action = 'optm_take_pictures'
    elif daily_cp_details[2] == '1' and daily_cp_details[15] == 'YES':
        action='optm_Process_Image'

    elif daily_cp_details[2] =='2' and daily_cp_details[15] == 'YES':
        action = 'optm_Dump'
    else:
        action = 'optm_idle'

    # data from exported data format - start time| end time| action- optm for optimized| memory | pictures in memory| processed images in memory| photos downloaded
    constraint_land_list.append(
        [(dt.timedelta(seconds=(int(daily_cp_details[0])))), (dt.timedelta(seconds=int(daily_cp_details[1]))), action, daily_cp_details[4], float(daily_cp_details[5]), daily_cp_details[9], daily_cp_details[11],
         daily_cp_details[7],float(daily_cp_details[13])])

onboard_mem = (0.8 * 24 * 10 ** 5)

# Overall data for two plots.
data = {'Time':[str(constraint_land_list[i][0]) for i in range (0, len(constraint_land_list))],
        'Alternate_Memory':[(a1_attack[i][4])for i in range (0, len(a1_attack))],
        'Max_Memory':[(onboard_mem)for i in range (0, len(constraint_land_list))],
        'Initial_Memory':[(constraint_land_list[i][3])for i in range (0, len(constraint_land_list))],
        'Pics': [(constraint_land_list[i][4]) for i in range(0, len(constraint_land_list))],
        'Process': [str(float(constraint_land_list[i][7]) / float(image_mem / process_im_mem)) for i in range(0, len(constraint_land_list))],
        'Dump': [str(float(constraint_land_list[i][8])) for i in range(0, len(constraint_land_list))]}

z = pd.DataFrame(data=data)

# Data points for first plot.
z['Time'] = pd.to_datetime(z['Time'])
z['Alternate_Memory'] = z['Alternate_Memory'].astype(float)
z['Initial_Memory'] = z['Initial_Memory'].astype(float)
z['Max_Memory'] = z['Max_Memory'].astype(float)

z = z[["Time",'Alternate_Memory','Initial_Memory', "Max_Memory"]].set_index("Time")

# Data points for second plot.
z1 = pd.DataFrame(data=data)
z1['Time'] = pd.to_datetime(z1['Time'])
z1['Process'] = z1['Process'].astype(float)
z1['Dump'] = z1['Dump'].astype(float)
z1 = z1[["Time", "Pics", "Process", "Dump"]].set_index("Time")

ax1 = z.plot(grid=True)

# Combine two plots into 1 and customize colors.
ax2 = ax1.twinx()
z.Max_Memory.plot(ax=ax2, color='green', label='Max_Memory')
z.Alternate_Memory.plot(ax=ax2, color='blue', label='Alternate_Memory')
z.Initial_Memory.plot(ax=ax2, color='orange', label='Initial_Memory')
z1.Pics.plot(ax=ax1, color='purple', label='Images')
z1.Process.plot(ax=ax1, color='cyan', label='Process')
z1.Dump.plot(ax=ax1, color='red', label='Down-link')

# Set axes labels and format.
ax1.set_ylabel('No. Of Images in Memory', fontsize=20)
ax1.set_xlabel('Time', fontsize=20)
ax2.set_ylabel('Initial_Memory', fontsize=20)
ax2.legend(bbox_to_anchor=(0.8, 1.00))
ax1.legend(bbox_to_anchor=(1.08, 1.12), fontsize=15, ncol=6)
ax2.set_ylim([-60000, 2000000])
ax1.set_ylim([-20, 800])
ax1.tick_params(labelsize=15)
ax2.tick_params(labelsize=15)
ax1.grid('on', which='minor', axis='x')
ax1.tick_params(which='minor',axis='x',labelsize=15)
ax1.set_title('Day ' + str(day), fontsize=20, x=0.5, y=1.1)

# Remove duplicate legend.
ax2.get_legend().remove()

myFmt = DateFormatter("%H:%M:%S")
plt.gcf().set_size_inches(15,8)
plt.savefig(line_file)
plt.show()


