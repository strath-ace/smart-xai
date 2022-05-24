import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
from matplotlib.dates import DateFormatter


day = 3

line_file= 'SEP_Results/Day/line_argument' + str(day) + '.png'

# load a1 attack file


action_a1_path = 'SEP_Results/Day/Attack_violation_summary_a12' + str(day) + '.txt'
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
    #print((dt.timedelta(seconds=(int(start_time)))))

cp_path = 'SEP_Results/Day/Optimized_Results' + str(day) + '.txt'
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
#for i in range(283, 3488):
for i in range(1, 17278):
    daily_cp_details = lines_cp_coord[i].split()
    # time_start_2 = daily_cp_details[6]
    # memory =daily_cp_details[7]

    if daily_cp_details[2]  == '0':
        action = 'optm_take_pictures'
    elif daily_cp_details[2] == '1':
        action='optm_Process_Image'
    # elif daily_cp_details[2] == '2':
    #     action = 'optm_Calibrate'
    elif daily_cp_details[2] =='2':
        action = 'optm_Dump'
    else:
        action = 'optm_idle'

    #data from exported data format - start time| end time| action- optm for optimized| memory | pictures in memory| processed images in memory| photos downloaded
    constraint_land_list.append(
        [(dt.timedelta(seconds=(int(daily_cp_details[0])))), (dt.timedelta(seconds=int(daily_cp_details[1]))), action, daily_cp_details[4], float(daily_cp_details[5]), daily_cp_details[9], daily_cp_details[11]])


onboard_mem = (0.8 * 24 * 10 ** 5)
data = {'Time':[str(constraint_land_list[i][0]) for i in range (0, len(constraint_land_list))],
        'New_Memory':[(a1_attack[i][4])for i in range (0, len(a1_attack))],
        'Max_Memory':[(onboard_mem)for i in range (0, len(constraint_land_list))],
        'Initial_Memory':[(constraint_land_list[i][3])for i in range (0, len(constraint_land_list))]}

data1 = {'Time':[str(constraint_land_list[i][0]) for i in range (0, len(constraint_land_list))],
        'New_Memory':[(a1_attack[i][4])for i in range (0, len(a1_attack))]}

z = pd.DataFrame(data=data)

z['Time'] = pd.to_datetime(z['Time'])
z['New_Memory'] = z['New_Memory'].astype(float)
z['Initial_Memory'] = z['Initial_Memory'].astype(float)
z['Max_Memory'] = z['Max_Memory'].astype(float)

z = z[["Time",'New_Memory','Initial_Memory', "Max_Memory"]].set_index("Time")

plt.rcParams.update({'font.size': 20})
# z1 = pd.DataFrame(data=data1)
# z1['Time'] = pd.to_datetime(z1['Time'])
# z1['New_Memory'] = z1['New_Memory'].astype(float)
# z1 = z1[["Time",'New_Memory']].set_index("Time")
myFmt = DateFormatter("%H:%M:%S")
ax1 =z.plot(grid=True)
ax1.grid('on', which='minor', axis='x' )
plt.legend(fontsize=20)

plt.gcf().set_size_inches(15, 8)
plt.savefig(line_file)
plt.show()




#myFmt = DateFormatter("%H:%M:%S")

# ax1 =z.plot(grid=True)
#
# ax2=ax1.twinx()
# z1.Memory.plot(ax=ax2, color='purple', label='Memory')
# z1.Max_Memory.plot(ax=ax2, color='grey', label='Max_Memory',linestyle='dashed')
# ax1.set_ylabel('No. Of Images')
# ax2.set_ylabel('Memory')
# ax2.legend(bbox_to_anchor=(0.9, 1.1))
# ax1.legend(bbox_to_anchor=(0.3, 1.1),ncol=len(df.columns))
# #ax1.legend(loc="upper center")
# ax1.grid('on', which='minor', axis='x' )
#(QT backend)
# mng = plt.get_current_fig_manager()
# mng.resize(*mng.window.maxsize())
#plt.tight_layout()
#plt.show()


#z.Memory.plot(ax=ax1, color='purple', label='Memory')
#z.Max_Memory.plot( color='grey', label='Max_Memory',linestyle='dashed')

