# ------------------ Copyright (C) 2022 University of Strathclyde and Author ---------------------------------
# --------------------------------- Author: Cheyenne Powell -------------------------------------------------
# ------------------------- e-mail: cheyenne.powell@strath.ac.uk --------------------------------------------

# File 3 b- This file creates a summary following an attack of action a1 on other actions at selected time t,\
# to the rest of the schedule.
# ===========================================================================================================


import pandas as pd


def mem_vio (day, filename):
 # day = 3

    filename1 = filename + '/Attack_violation_summary_a12' + str(day) + '.txt'

    # load of optimized schedule information
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
    attack_summary1 = [['i', 'start_time', 'S', 'a', 'm', 'objective_value', 'violation', 'time_of_incident', 'mi1', 'final_objective', 'feasible_better', 'S_Objective']]

    i = 1

    # attack is scheduled to take place at instance "15178" time 75886 seconds => 21:04:00, can be altered for any time, to see the effect of a1 on other actions.
    while i in range(1, 15178):

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

        mi_a1 = m1

        # Tabulate up to the point where an attack occurs.
        if i < 15177:
            mi_a1 = mi
            attack_summary1.append([i, start_time, S, a1, mi, 0, 'Not_exceeded', start_time, mi_a1, 0, 0, S_Objective])

        # When the attack time is reached, the alternate memory is created and cascaded throughout.
        elif a1 == '-':

            for n in range(i, count_coord - 1):

                # Initial schedule loaded.
                solver_values = lines_cp_coord[n].split()
                start_time2 = int(solver_values[0])

                # Schedule taken from attack profile created from "sep_data_sort".
                S_1 = lines_attack_coord[n].split()[4]

                if n == i:
                    mi_a1 = m1
                    objective_value = 1 + int(solver_values[6])

                # Calculate new memory following schedule attack.
                else:
                    if S_1 == '0':
                        mi_a1 = mi_a1 + ma1
                    elif S_1 == '1':
                        mi_a1 = mi_a1 + ma2
                    elif S_1 == '2':
                        mi_a1 = mi_a1 + ma3
                    else:
                        mi_a1 = mi_a1

                    objective_value = 0

                # Recalculate new objective.
                objective_value1 = 1 + int(solver_values[6])

                # Check if memory is exceeded.
                if mi_a1 > m_max or mi_a1 <= 0:
                    violation1 = 'Exceeded'
                    a1 = '-'
                    objective_value1 = objective_value
                    final_objective1 = S_Objective_process + S_Objective_download + objective_value1
                    feasible_better1 = 'Infeasible'

                    attack_summary1.append([i, start_time, S, a1, mi, objective_value1, violation1, start_time2, mi_a1, final_objective1, feasible_better1, S_Objective])

                else:
                    if n == count_coord - 1:
                        violation1 = 'Not_exceeded'
                    else:
                        violation1 = 'Not_exceeded'
                    a1 = '-'

                    objective_value1 = objective_value1
                    final_objective1 = S_Objective_process + S_Objective_download + objective_value1

                    if final_objective1 >= S_Objective:
                        feasible_better1 = 'Feasible_better_objective'
                    elif final_objective1 < S_Objective and violation1 == 'Exceeded':
                        feasible_better1 = 'Infeasible'
                    else:
                        feasible_better1 = 'Feasible_worse_objective'
                    attack_summary1.append([i, start_time, S, a1, mi, objective_value1, violation1, start_time2, mi_a1, final_objective1, feasible_better1, S_Objective])

        i = i + 1

    # Save file.
    file1 = open(filename1, 'w')
    df = pd.DataFrame(attack_summary1)
    file1.writelines(df.to_string(header=False, index=False))
    file1.close()
