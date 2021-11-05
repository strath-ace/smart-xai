import pandas as pd
import datetime as dt
from Sentinel_2A_Case_Study.Environment.start_end_points_data import time_select


def manual_data_retrieved(path, time_interval, day, month):
    memory_states = path + '/manual_memory_states_seconds' + str(day) + '.txt'
    file = open(path + '/binary_daily_schedule' + str(day) + '.txt', 'w')
    memory_coord = open(memory_states, "r")
    memory_count_coord = 0
    for line in memory_coord:
        if line != "\n":
            memory_count_coord += 1
    memory_coord.close()

    memory_coord = open(memory_states, "r")
    # print(line_count)
    memory_count_coord = memory_count_coord
    memory_coord = memory_coord.read()
    memory_coord = memory_coord.split('\n')

    start_second_interval, end_second_interval = time_select(day, month)
    manual_list = []
    mem_data_list = []
    for i in range(0, memory_count_coord):
        memory_details = memory_coord[i].split()

        if memory_details[5] > '0':
            if memory_details[2] == '1' and memory_details[6] == 'True':
                action = 0
            elif memory_details[2] == '2' and memory_details[6] == 'True':
                action = 1
            # elif memory_details[2] == '3':
            #     action = 'man_Calibrate'
            elif memory_details[2] == '4' and memory_details[6] == 'True':
                action = 2
            else:
                action = -1
        else:
            action = -1

        manual_list.append([memory_details[0], memory_details[1], memory_details[2], action, memory_details[3], memory_details[6], memory_details[5]])

    # print(len(manual_list))

    for i in range(0, len(manual_list)):

        mem_start = int(manual_list[i][0])
        # elif i == memory_count_coord:
        mem_end = int(manual_list[i][1])

        if i == 0:
            e = start_second_interval
        else:
            e = (mem_data_list[len(mem_data_list) - 1][1])

        while e >= start_second_interval and (e < mem_end):

            if e < mem_start:
                mem_access = 0
            elif e in range(mem_start, mem_end):
                mem_access = manual_list[i][3]
            else:
                mem_access = 0

            mem_data_list.append([e, e + time_interval, mem_access])
            e += time_interval

        g = (mem_data_list[len(mem_data_list) - 1][1])
        while (g >= mem_end) and (g <= end_second_interval) and (i >= len(manual_list) - 1):
            mem_access = 0
            mem_data_list.append([g, g + time_interval, mem_access])
            g += time_interval

    #convert seconds to time H:M:S
    mem_data_list_time=[]
    for i in range(0, len(mem_data_list)):
        mem_data_list_time.append([str(dt.timedelta(seconds=(mem_data_list[i][0]))),str(dt.timedelta(seconds=(mem_data_list[i][1]))),mem_data_list[i][2]])

    df = pd.DataFrame(mem_data_list_time)
    file.writelines(df.to_string(header=False, index=False))
    return mem_data_list, mem_data_list_time
