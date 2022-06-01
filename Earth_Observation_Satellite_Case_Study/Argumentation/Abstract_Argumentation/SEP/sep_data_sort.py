# file number 2 - used to create the initial argumentation documents

import pandas as pd


# if a conflict with action 1 occurs for images to be taken
def a1_action(a1, memory1):
    if a1 == '0':
        action_1 = '-'
        m1 = memory1
    else:
        m1 = 0
        action_1 = 'N/A'
    return action_1, m1


# if a conflict occurs for action 2 (image processing) to occur
def a2_action(a2, memory2):
    if a2 == '1':
        action_2 = '-'
        m2 = memory2
    else:
        m2 = 0
        action_2 = 'N/A'
    return action_2, m2


# if a conflict occurs for action 3 (down-linking) to take place
def a3_action(a3, memory3):
    if a3 == '2':
        action_3 = '-'
        m3 = memory3
    else:
        m3 = 0
        action_3 = 'N/A'
    return action_3, m3


def attack_summary():
    day = 3
    # interval = 3000
    # onboard memory is 80% of total memory
    onboard_mem = int(0.8 * 24 * 10 ** 5)

    filename1 = 'SEP_Results/Day/Argumentation' + str(day) + '.txt'

    solver_path = 'SEP_Results/Day/Day' + str(day) + '.txt'
    solver_coord = open(solver_path, "r")
    count_coord = 0
    # for loop to count the number of lines in file
    for line in solver_coord:
        if line != "\n":
            count_coord += 1
    solver_coord.close()
    print(count_coord)

    # load data line by line
    solver_coord = open(solver_path, "r")
    content_cp_coord = solver_coord.read()
    lines_cp_coord = content_cp_coord.split('\n')
    # print(lines_cp_coord)

    final_list = [['start_time', 'land', 'station', 'day', 'S*', 'mi', 'a1', 'a2', 'a3', 'mi1', 'mi2', 'mi3', 'Mmax']]
    # changing data format
    for i in range(1, count_coord):
        SEP_data = lines_cp_coord[i].split()
        # print(SEP_data)
        land = SEP_data[1]
        station = SEP_data[2]
        day = SEP_data[3]
        S = int(SEP_data[4])
        mi = int(SEP_data[5])
        a1 = SEP_data[7]
        a2 = SEP_data[11]
        a3 = SEP_data[15]
        m1 = SEP_data[8]
        m2 = SEP_data[12]
        m3 = SEP_data[16]
        start_time = SEP_data[0]

        # Check what actions are scheduled followed by the conflict conditions
        if S == 0:
            action_1 = 'N/A'
            m1 = 0
            # if action 2 conflict is present
            action_2, m2 = a2_action(a2, m2)
            # if action 3 conflict is present
            action_3, m3 = a3_action(a3, m3)

        elif S == 1:
            action_2 = 'N/A'
            m2 = 0
            # if action 1 conflict is present
            action_1, m1 = a1_action(a1, m1)
            # if action 3 conflict is present
            action_3, m3 = a3_action(a3, m3)

        elif S == 2:
            action_3 = 'N/A'
            m3 = 0
            # if action 1 conflict is present
            action_1, m1 = a1_action(a1, m1)
            # if action 2 conflict is present
            action_2, m2 = a2_action(a2, m2)

        else:
            # if action 1 conflict is present
            action_1, m1 = a1_action(a1, m1)
            # if action 2 conflict is present
            action_2, m2 = a2_action(a2, m2)
            # if action 3 conflict is present
            action_3, m3 = a3_action(a3, m3)
        final_list.append([start_time, land, station, day, S, mi, action_1, action_2, action_3, m1, m2, m3, onboard_mem])

    # Write data to file
    file1 = open(filename1, 'w')
    df = pd.DataFrame(final_list)
    file1.writelines(df.to_string(header=False, index=False))
    file1.close()


attack_summary()
