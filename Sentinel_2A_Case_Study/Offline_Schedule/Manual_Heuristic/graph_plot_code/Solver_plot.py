# function used for creating the line plot for the generated schedule by the solver

import datetime as dt
import matplotlib.dates as mdates
import pandas as pd
from matplotlib import pyplot as plt


def solver_plot(day, path, solver_plot_image, image_mem, process_im_mem, onboard_mem, Max_pictures):
    constraint_land_list = []

    cp_coord = open(path, "r")
    cp_count_coord = 0
    for line in cp_coord:
        if line != "\n":
            cp_count_coord += 1
    cp_coord.close()

    daily_cp_coord = open(path, "r")
    # print(line_count)
    cp_count_coord = cp_count_coord
    content_cp_coord = daily_cp_coord.read()
    lines_cp_coord = content_cp_coord.split('\n')

    for i in range(0, cp_count_coord):
        daily_cp_details = lines_cp_coord[i].split()
        # print(daily_cp_details[13])
        if daily_cp_details[2] == '0' and daily_cp_details[15] == 'YES':
            action = 'optm_take_pictures'
        elif daily_cp_details[2] == '1' and daily_cp_details[15] == 'YES':
            action = 'optm_Process_Image'
        # elif daily_cp_details[2] == '3':
        #     action = 'optm_Calibrate'
        elif daily_cp_details[2] == '2' and daily_cp_details[15] == 'YES':
            action = 'optm_Dump'
        else:
            action = 'optm_idle'

        # data from exported data format - start time| end time| action- optm for optimized| memory | pictures in memory| processed images in memory| photos downloaded
        constraint_land_list.append(
            [(dt.timedelta(seconds=(int(daily_cp_details[0])))), (dt.timedelta(seconds=int(daily_cp_details[1]))), action, daily_cp_details[4], float(daily_cp_details[5]), daily_cp_details[7],
             float(daily_cp_details[13])])

    i = 0
    constraints = []
    while i in range(0, len(constraint_land_list)):
        constraints.append(
            [constraint_land_list[i][0], constraint_land_list[i][1], constraint_land_list[i][2], constraint_land_list[i][3], constraint_land_list[i][4], constraint_land_list[i][5], constraint_land_list[i][6]])
        i += 1

    data = {'Time': [str(constraints[i][0]) for i in range(0, len(constraints))],
            'Memory': [str(constraints[i][3]) for i in range(0, len(constraints))],
            'Max_Memory': [onboard_mem for _ in range(0, len(constraints))],
            'Max_pics': [Max_pictures for _ in range(0, len(constraints))],
            'Pics': [(constraints[i][4]) for i in range(0, len(constraints))],
            'Process': [str(float(constraints[i][5]) / float(image_mem / process_im_mem)) for i in range(0, len(constraints))],
            'Dump': [str(float(constraints[i][6])) for i in range(0, len(constraints))]}

    z = pd.DataFrame(data=data)
    # z["Date"] = "2019-09-09"
    z['Time'] = pd.to_datetime(z['Time'], format='%H:%M:%S')

    z['Time'] = mdates.date2num(z['Time'])
    # print(z['Time'])
    z['Process'] = z['Process'].astype(float)
    z['Dump'] = z['Dump'].astype(float)
    z['Memory'] = z['Memory'].astype(int)
    z['Max_pics'] = z['Max_pics'].astype(float)
    z['Max_Memory'] = z['Max_Memory'].astype(float)
    z = z[["Time", "Pics", "Process", "Dump", 'Max_pics']].set_index("Time")

    z1 = pd.DataFrame(data=data)
    z1['Time'] = pd.to_datetime(z1['Time'], format='%H:%M:%S')
    z1['Time'] = mdates.date2num(z1['Time'])
    z1['Process'] = z1['Process'].astype(float)
    z1['Dump'] = z1['Dump'].astype(float)
    z1['Memory'] = z1['Memory'].astype(int)
    z1['Max_pics'] = z1['Max_pics'].astype(float)
    z1['Max_Memory'] = z1['Max_Memory'].astype(float)
    z1 = z1[["Time", "Memory", "Max_Memory"]].set_index("Time")

    ax1 = z.plot(grid=True)

    ax2 = ax1.twinx()
    z1.Memory.plot(ax=ax2, color='purple', label='Memory')
    z1.Max_Memory.plot(ax=ax2, color='grey', label='Max_Memory', linestyle='dashed')
    ax1.set_ylabel('No. Of Images in Memory', fontweight='bold', fontsize=15)
    ax1.set_xlabel('Day ' + str(day), fontweight='bold', fontsize=15)
    ax2.set_ylabel('Memory', fontweight='bold', fontsize=15)
    ax2.legend(bbox_to_anchor=(0.9, 1.1))
    ax1.legend(bbox_to_anchor=(0.3, 1.1), ncol=len(z.columns))
    ax2.set_ylim([-60000, 2000000])
    ax1.set_ylim([-20, 800])
    ax1.grid('on', which='minor', axis='x')

    plt.gcf().set_size_inches(15, 8)
    myFmt = mdates.DateFormatter('%H:%M:%S')
    ax1.xaxis.set_major_formatter(myFmt)
    # plt.show()
    plt.savefig(solver_plot_image)

    return constraint_land_list
