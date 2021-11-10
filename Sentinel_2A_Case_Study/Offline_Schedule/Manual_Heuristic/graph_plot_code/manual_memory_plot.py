# Function used for plotting the line graph for the manual day schedule

import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.dates as mdates


def manual_memory_plot(day, path, path1, manual_plot_image):
    memory_land_list = []
    memory_coord = open(path, "r")
    memory_count_coord = 0
    for line in memory_coord:
        if line != "\n":
            memory_count_coord += 1
    memory_coord.close()

    memory_coord = open(path, "r")
    # print(line_count)
    memory_count_coord = memory_count_coord
    memory_coord = memory_coord.read()
    memory_coord = memory_coord.split('\n')

    for i in range(0, memory_count_coord):
        memory_details = memory_coord[i].split()
        memory_land_list.append(
            [memory_details[0], memory_details[1], memory_details[2], memory_details[3], memory_details[4], memory_details[5], memory_details[6], memory_details[7], memory_details[8], memory_details[9],
             memory_details[10]])

    memory_land_list_binary = []
    binary_memory_coord = open(path1, "r")
    binary_memory_count_coord = 0
    for line in binary_memory_coord:
        if line != "\n":
            binary_memory_count_coord += 1
    binary_memory_coord.close()

    binary_memory_coord = open(path1, "r")
    # print(line_count)
    binary_memory_count_coord = binary_memory_count_coord
    binary_memory_coord = binary_memory_coord.read()
    binary_memory_coord = binary_memory_coord.split('\n')

    for i in range(0, binary_memory_count_coord):
        # print(binary_memory_count_coord)
        binary_memory_details = binary_memory_coord[i].split()

        if binary_memory_details[2] == '0':
            action = 'man_take_pictures'
        elif binary_memory_details[2] == '1':
            action = 'man_process_Image'
        # elif memory_details[2] == '3':
        #     action = 'man_Calibrate'
        elif binary_memory_details[2] == '2':
            action = 'man_dump'
        else:
            action = 'man_idle'

        memory_land_list_binary.append(
            [binary_memory_details[0], binary_memory_details[1], action])

    # line graph for manual data
    data1 = {'Time': [str(memory_land_list[i][0]) for i in range(0, len(memory_land_list))],
             'Memory': [(memory_land_list[i][5]) for i in range(0, len(memory_land_list))],
             'Pics': [(memory_land_list[i][7]) for i in range(0, len(memory_land_list))],
             'Process': [str(float(memory_land_list[i][8])) for i in range(0, len(memory_land_list))],
             'Dump': [str(float(memory_land_list[i][9])) for i in range(0, len(memory_land_list))]}

    x = pd.DataFrame(data=data1)
    x['Time'] = pd.to_datetime(x['Time'])
    x['Pics'] = x['Pics'].astype(float)
    x['Process'] = x['Process'].astype(float)
    x['Dump'] = x['Dump'].astype(float)
    x['Memory'] = x['Memory'].astype(float)
    x = x[["Time", "Pics", "Process", "Dump"]].set_index("Time")

    x1 = pd.DataFrame(data=data1)
    x1['Time'] = pd.to_datetime(x1['Time'])
    x1['Pics'] = x1['Pics'].astype(float)
    x1['Process'] = x1['Process'].astype(float)
    x1['Dump'] = x1['Dump'].astype(float)
    x1['Memory'] = x1['Memory'].astype(float)
    x1 = x1[["Time", "Memory"]].set_index("Time")

    myFmt1 = mdates.DateFormatter("%H:%M:%S")

    ax3 = x.plot(grid=True)

    ax4 = ax3.twinx()
    x1.Memory.plot(ax=ax4, color='purple', label='Memory')
    ax3.set_ylabel('No. Of Images in Memory', fontweight='bold', fontsize=15)
    ax3.set_xlabel('Day ' + str(day), fontweight='bold', fontsize=15)
    ax4.set_ylabel('Memory', fontweight='bold', fontsize=15)
    ax4.legend(bbox_to_anchor=(0.9, 1.1))
    ax3.legend(bbox_to_anchor=(0.3, 1.1), ncol=len(x.columns))
    ax4.set_ylim([0, 2000000])
    ax3.set_ylim([-20, 800])
    ax3.grid('on', which='minor', axis='x')
    plt.gcf().set_size_inches(15, 8)

    ax3.xaxis.set_major_formatter(myFmt1)

    plt.savefig(manual_plot_image)  # , dpi=1500)

    return memory_land_list_binary
