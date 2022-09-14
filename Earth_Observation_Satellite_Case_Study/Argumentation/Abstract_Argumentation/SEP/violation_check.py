# ------------------ Copyright (C) 2022 University of Strathclyde and Author ---------------------------------
# --------------------------------- Author: Cheyenne Powell -------------------------------------------------
# ------------------------- e-mail: cheyenne.powell@strath.ac.uk --------------------------------------------

# File 3 a -This file checks if there is a violation of the onboard memory when an action at any point in\
# time is replaced with another.
# used to calculate the objective each time SEP is used and determine if the result for each action is\
# feasible with a better objective or feasible with a worse objective - used for optimality. NOT NEEDED FOR FEASIBILITY
# ===========================================================================================================

import pandas as pd



# function to calculate if each SEP change is feasible - meaning if an action replaces an existing action, will the memory be exceeded later?
def SEP_action_a(chosen_action, a, m, i, ma1, ma2, ma3, S_Objective_value1, S_Objective_value2, count_coord, lines_cp_coord, lines_attack_coord, S , m_max):
    mi_a = m
    final_objective = 0
    objective_value1 = 0
    violation1 = ''
    start_time2 = 0

    for n in range(i, count_coord - 1):

        solver_values = lines_cp_coord[n].split()
        start_time2 = int(solver_values[0])
        S_1 = lines_attack_coord[n].split()[4]

        if S == '0' or S == '1':
            obj = 1
        elif S == '2':
            obj = 2
        else:
            obj = 0

        # If the action to be executed is 1,2 or 3 excluding 4
        if chosen_action == 1:
            obj_val_for_action = 1 + int(solver_values[6]) - obj
        elif chosen_action == 2:
            obj_val_for_action = 1 + int(solver_values[8]) - obj
        elif chosen_action == 3:
            obj_val_for_action = 2 * (1 + int(solver_values[10])) - obj
        else:
            obj_val_for_action = 'error'

        # Calculation for alternate memory values
        if n == i:
            mi_a = m
            objective_value = obj_val_for_action
        else:
            if S_1 == '0':
                mi_a = mi_a + ma1
            elif S_1 == '1':
                mi_a = mi_a + ma2
            elif S_1 == '2':
                mi_a = mi_a + ma3
            else:
                mi_a = mi_a

            objective_value = 0
            final_objective = 0

        # recalculate new objective
        objective_value1 = obj_val_for_action

        # check if memory is exceeded
        if mi_a > m_max or mi_a <= 0:
            violation1 = 'Exceeded'
            a = '-'
            objective_value1 = objective_value

            break
        else:
            if n == count_coord - 1:
                violation1 = 'Not_exceeded'
            else:
                violation1 = 'Not_exceeded'
            a = '-'
            objective_value1 = objective_value1

            final_objective = (S_Objective_value1 + S_Objective_value2 + objective_value1)

    return i, a, objective_value1, violation1, start_time2, mi_a, final_objective


def feasible_better(day, filename):
    # day = 3

    filename1 = filename + '/Attack_summary_ap' + str(day) + '.txt'
    filename2 = filename + '/Attack_summary_ar' + str(day) + '.txt'
    filename3 = filename +'/Attack_summary_ad' + str(day) + '.txt'

    # load of solvers information
    solver_path = '../../../Offline_Schedule/Results_with max(pic,proc,down)/Day ' + str(day) + '/Solver/Optimized_results' + str(day) + '.txt'
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


    # load of attack information
    attack_path = filename + '/Argumentation' + str(day) + '.txt'
    attack_coord = open(attack_path, "r")
    count_attack_coord = 0
    # for loop to count the number of lines in file
    for line in attack_coord:
        if line != "\n":
            count_attack_coord += 1
    attack_coord.close()
    print(count_attack_coord)
    # load data line by line
    attack_coord = open(attack_path, "r")
    attack_cp_coord = attack_coord.read()
    lines_attack_coord = attack_cp_coord.split('\n')

    time_interval = 5
    # onboard memory is 80% of total memory 2TB - 1,920,000
    onboard_mem = int(0.8 * 24 * 10 ** 5)
    #  memory required per image
    image_mem = 2688
    # downlink data rate
    downlink_data_rate = 280 * 2 * time_interval
    # 5000Kbit/s to process images
    process_im_mem = 50 * time_interval

    S_Objective = int(lines_cp_coord[count_coord - 2].split()[6]) + int(lines_cp_coord[count_coord - 1].split()[8]) + \
                  (2 * int(lines_cp_coord[count_coord - 2].split()[10]))

    S_Objective_image = int(lines_cp_coord[count_coord - 2].split()[6])
    S_Objective_process = int(lines_cp_coord[count_coord - 2].split()[8])
    S_Objective_download = (2 * int(lines_cp_coord[count_coord - 2].split()[10]))
    print(S_Objective_image, S_Objective_process, S_Objective_download)

    # Headings created to summarize each action attack on the schedule.
    attack_summary1 = [['i', 'start_time', 'S', 'ap', 'objective_value', 'violation', 'time_of_incident', 'mi1', 'final_objective', 'feasible_better', 'S_Objective']]
    attack_summary2 = [['i', 'start_time', 'S', 'ar', 'objective_value', 'violation', 'time_of_incident', 'mi2', 'final_objective', 'feasible_better', 'S_Objective']]
    attack_summary3 = [['i', 'start_time', 'S', 'ad', 'objective_value', 'violation', 'time_of_incident', 'mi3', 'final_objective', 'feasible_better', 'S_Objective']]

    # To go through the schedule for each action and where an attack can occur is recorded.
    i = 1
    while i in range(1, count_attack_coord):
        attack_data = lines_attack_coord[i].split()
        start_time = int(attack_data[0])
        end_time = start_time + time_interval
        land = attack_data[1]
        station = attack_data[2]
        day = attack_data[3]
        S = attack_data[4]
        mi = int(attack_data[5])
        a1 = attack_data[6]
        a2 = attack_data[7]
        a3 = attack_data[8]
        m1 = int(attack_data[9])
        m2 = int(attack_data[10])
        m3 = int(attack_data[11])
        m_max = int(attack_data[12])

        ma1 = image_mem
        ma2 = process_im_mem
        ma3 = -downlink_data_rate

        # Used to check the feasibility of each action when an attack takes place on each action.
        # Image taking attacks.
        if a1 == '-':
            i, a1, objective_value1, violation1, start_time1, mi1, final_objective1 = SEP_action_a(1, a1, m1, i, ma1, ma2, ma3, S_Objective_process, S_Objective_download, count_coord,lines_cp_coord,lines_attack_coord, S, m_max)
            if final_objective1 >= S_Objective:
                feasible_better1 = 'Feasible_better_objective'
            elif final_objective1 < S_Objective and violation1 == 'Exceeded':
                feasible_better1 = 'Infeasible'
            else:
                feasible_better1 = 'Feasible_worse_objective'
            attack_summary1.append([i, start_time, S, a1, objective_value1, violation1, start_time1, mi1, final_objective1, feasible_better1,S_Objective])

        # Processing of an image, action attack.
        if a2 == '-':
            i, a2, objective_value2, violation2, start_time2, mi2, final_objective2 = SEP_action_a(2, a2, m2, i, ma1, ma2, ma3, S_Objective_image, S_Objective_download, count_coord,lines_cp_coord,lines_attack_coord, S, m_max)
            if final_objective2 >= S_Objective:
                feasible_better2 = 'Feasible_better_objective'
            elif final_objective2 < S_Objective and violation2 == 'Exceeded':
                feasible_better2 = 'Infeasible'
            else:
                feasible_better2 = 'Feasible_worse_objective'
            attack_summary2.append([i, start_time, S, a2, objective_value2, violation2, start_time2, mi2, final_objective2, feasible_better2, S_Objective])

        # Down-linking of an image action attack.
        if a3 == '-':
            i, a3, objective_value3, violation3, start_time3, mi3, final_objective3 = SEP_action_a(3, a3, m3, i, ma1, ma2, ma3, S_Objective_image, S_Objective_process, count_coord,lines_cp_coord,lines_attack_coord, S, m_max)
            if final_objective3 >= S_Objective:
                feasible_better3 = 'Feasible_better_objective'
            elif final_objective3 < S_Objective and violation3 =='Exceeded':
                feasible_better3 = 'Infeasible'
            else:
                feasible_better3 = 'Feasible_worse_objective'
            attack_summary3.append([i, start_time, S, a3, objective_value3, violation3, start_time3, mi3, final_objective3, feasible_better3, S_Objective])

        i = i + 1

    # Save file.
    file1 = open(filename1, 'w')
    df = pd.DataFrame(attack_summary1)
    file1.writelines(df.to_string(header=False, index=False))
    file1.close()

    file1 = open(filename2, 'w')
    df = pd.DataFrame(attack_summary2)
    file1.writelines(df.to_string(header=False, index=False))
    file1.close()

    file1 = open(filename3, 'w')
    df = pd.DataFrame(attack_summary3)
    file1.writelines(df.to_string(header=False, index=False))
    file1.close()
