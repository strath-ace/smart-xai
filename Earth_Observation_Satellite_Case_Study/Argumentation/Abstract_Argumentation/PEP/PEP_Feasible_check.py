# ------------------ Copyright (C) 2022 University of Strathclyde and Author ---------------------------------
# --------------------------------- Author: Cheyenne Powell -------------------------------------------------
# ------------------------- e-mail: cheyenne.powell@strath.ac.uk --------------------------------------------

# PEP calculation 2 - checks for feasibility with pair exchanges.
# Checks which action of the 2 appears first in the schedule, to then swap and calculate the memory
# change throughout until the first action (now the second) has been reached. Which then alters the memory at that
# instance to then cascade the change throughout the rest of the schedule.
# Note: Actions were given numbers idle - '-1', image taking - '0', processing - '1', and down-linking - '2'.
# ===========================================================================================================

from Earth_Observation_Satellite_Case_Study.Argumentation.Abstract_Argumentation.PEP.PEP_calc import pep_action_a

day = 3

# Load of attacks summary information.
attack_path = '../SEP_Results/Day/Argumentation' + str(day) + '.txt'
attack_coord = open(attack_path, "r")
count_attack_coord = 0

# For loop to count the number of lines in file.
for line in attack_coord:
    if line != "\n":
        count_attack_coord += 1
attack_coord.close()
print(count_attack_coord)

# load data line by line.
attack_coord = open(attack_path, "r")
attack_cp_coord = attack_coord.read()
lines_attack_coord = attack_cp_coord.split('\n')

solver_path = '../SEP_Results/Day/Optimized_results' + str(day) + '.txt'
solver_coord = open(solver_path, "r")
count_coord = 0

# For loop to count the number of lines in file.
for line in solver_coord:
    if line != "\n":
        count_coord += 1
solver_coord.close()
print(count_coord)

# load data line by line.
solver_coord = open(solver_path, "r")
content_cp_coord = solver_coord.read()
lines_cp_coord = content_cp_coord.split('\n')

# Time for every action is 5s.
time_interval = 5

# Onboard memory is 80% of total memory 2TB - 1,920,000.
onboard_mem = int(0.8 * 24 * 10 ** 5)

#  Memory required per image.
image_mem = 2688

# Downlink data rate.
downlink_data_rate = 280 * 2 * time_interval
process_im_mem = 50 * time_interval


def pep_check_swap(datastart, addr1, addr2, action_swap1, action_swap2):
    # Check to see which action of the 2 to be swapped occurs first to then make the swap and start with the
    # second action in the first action's place.
    if addr1 < addr2:
        start_point = datastart + addr1
        i = start_point
        start_time = int(lines_attack_coord[i].split()[0])
        addrx = datastart + addr2
    else:
        start_point = datastart + addr2
        i = start_point
        start_time = int(lines_attack_coord[i].split()[0])
        addrx = datastart + addr1

    # Idle action attack when actions are swapped is given a number 5 to differentiate from the other actions.
    action_idle_attack = 5
    action_swap_1_2 = -1

    # If function used to detect 'if' idle time is picked up in the schedule to be exchanged. The action,
    # idle is swapped with, is recorded.
    if action_swap2 == -1 or action_swap1 == -1:
        if [action_swap1, action_swap2] == [0, -1] or [action_swap1, action_swap2] == [-1, 0]:
            action_idle_attack = 0
        elif [action_swap1, action_swap2] == [1, -1] or [action_swap1, action_swap2] == [-1, 1]:
            action_idle_attack = 1
        elif [action_swap1, action_swap2] == [2, -1] or [action_swap1, action_swap2] == [-1, 2]:
            action_idle_attack = 2

    # If any of the other actions are detected, a value is given to assist with tracking the swap.
    else:
        if [action_swap1, action_swap2] == [0, 1] or [action_swap1, action_swap2] == [1, 0]:
            action_swap_1_2 = 0
        elif [action_swap1, action_swap2] == [0, 2] or [action_swap1, action_swap2] == [2, 0]:
            action_swap_1_2 = 1
        elif [action_swap1, action_swap2] == [1, 2] or [action_swap1, action_swap2] == [2, 1]:
            action_swap_1_2 = 2

    attack_data = lines_attack_coord[i].split()

    s = attack_data[4]
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
    idle = 'N/A'

    # Used to check if '0' is scheduled 's' (1) and if there is an attack by another action.
    if (a1 == '-') and s == '1' and (addr2 > addr1) and (action_swap_1_2 == 0):
        a_2 = '1'

        # PEP function called to do the memory calculations following the swap if the
        # memory constraint has been violated.
        i, a1, violation, start_time1, mi1, mi_a2 = \
            pep_action_a(a1, m1, i, ma1, ma2, ma3, count_coord, lines_cp_coord, lines_attack_coord, addrx, a_2, m_max,
                         addr1, addr2)
        if violation == 'Not_exceeded':
            violation = 'feasible'
            mem_violation = 1
        else:
            violation = 'Infeasible'
            mem_violation = 0
        swap_pos = int(lines_attack_coord[addrx].split()[0])
        a_1 = a1
        a_2 = '-' + str(swap_pos)
        attack_swap = [i, start_time, swap_pos, s, a_1, a_2, 'N/A', idle, mi, violation, mem_violation, start_time1,
                       mi1, mi_a2, 'N/A']

    # Used to check if '1' is scheduled 's' (0) and if there is an attack by another action.
    elif (a2 == '-') and s == '0' and (addr2 > addr1) and (action_swap_1_2 == 0):
        a_2 = '0'
        # PEP function called to do the memory calculations following the swap if the
        # memory constraint has been violated.
        i, a2, violation, start_time1, mi1, mi_a2 = \
            pep_action_a(a2, m2, i, ma1, ma2, ma3, count_coord, lines_cp_coord, lines_attack_coord, addrx, a_2, m_max,
                         addr1, addr2)
        if violation == 'Not_exceeded':
            violation = 'feasible'
            mem_violation = 1
        else:
            violation = 'Infeasible'
            mem_violation = 0
        swap_pos = int(lines_attack_coord[addrx].split()[0])
        a_1 = '-' + str(swap_pos)
        a_2 = a2
        attack_swap = [i, start_time, swap_pos, s, a_1, a_2, 'N/A', idle, mi, violation, mem_violation, start_time1,
                       mi1, mi_a2, 'N/A']


    # a1 attack a3 for swap  2,0
    elif (a1 == '-') and s == '2' and (addr2 > addr1) and (action_swap_1_2 == 1):
        a_3 = '2'
        i, a1, violation, start_time1, mi1, mi_a3 = \
            pep_action_a(a1, m1, i, ma1, ma2, ma3, count_coord, lines_cp_coord, lines_attack_coord, addrx, a_3, m_max,
                         addr1, addr2)
        if violation == 'Not_exceeded':
            violation = 'feasible'
            mem_violation = 1
        else:
            violation = 'Infeasible'
            mem_violation = 0
        swap_pos = int(lines_attack_coord[addrx].split()[0])
        a_1 = a1
        a_3 = '-' + str(swap_pos)
        attack_swap = [i, start_time, swap_pos, s, a_1, 'N/A', a_3, idle, mi, violation, mem_violation, start_time1,
                       mi1, 'N/A', mi_a3]


    # a3 attack a1 for swap  0,2
    elif (a3 == '-') and s == '0' and (addr2 > addr1) and (action_swap_1_2 == 1):
        a_3 = '0'
        i, a3, violation, start_time1, mi1, mi_a3 = \
            pep_action_a(a3, m3, i, ma1, ma2, ma3, count_coord, lines_cp_coord, lines_attack_coord, addrx, a_3, m_max,
                         addr1, addr2)
        if violation == 'Not_exceeded':
            violation = 'feasible'
            mem_violation = 1
        else:
            violation = 'Infeasible'
            mem_violation = 0
        swap_pos = int(lines_attack_coord[addrx].split()[0])
        a_1 = '-' + str(swap_pos)
        a_3 = a3
        attack_swap = [i, start_time, swap_pos, s, a_1, 'N/A', a_3, idle, mi, violation, mem_violation, start_time1,
                       mi1, 'N/A', mi_a3]


    # a2 attack a3 for swap  2,1
    elif (a2 == '-') and s == '2' and (addr2 > addr1) and (action_swap_1_2 == 2):
        a_3 = '2'
        i, a2, violation, start_time1, mi2, mi_a3 = \
            pep_action_a(a2, m2, i, ma1, ma2, ma3, count_coord, lines_cp_coord, lines_attack_coord, addrx, a_3, m_max,
                         addr1, addr2)
        if violation == 'Not_exceeded':
            violation = 'feasible'
            mem_violation = 1
        else:
            violation = 'Infeasible'
            mem_violation = 0
        swap_pos = int(lines_attack_coord[addrx].split()[0])
        a_2 = a2
        a_3 = '-' + str(swap_pos)
        attack_swap = [i, start_time, swap_pos, s, 'N/A', a_2, a_3, idle, mi, violation, mem_violation, start_time1,
                       'N/A', mi2, mi_a3]


    # 1,2
    elif (a3 == '-') and s == '1' and (addr2 > addr1) and (action_swap_1_2 == 2):
        a_3 = '1'
        i, a3, violation, start_time1, mi2, mi_a3 = \
            pep_action_a(a3, m3, i, ma1, ma2, ma3, count_coord, lines_cp_coord, lines_attack_coord, addrx, a_3, m_max,
                         addr1, addr2)
        if violation == 'Not_exceeded':
            violation = 'feasible'
            mem_violation = 1
        else:
            violation = 'Infeasible'
            mem_violation = 0
        swap_pos = int(lines_attack_coord[addrx].split()[0])
        a_2 = '-' + str(swap_pos)
        a_3 = a3
        attack_swap = [i, start_time, swap_pos, s, 'N/A', a_2, a_3, idle, mi, violation, mem_violation, start_time1,
                       'N/A', mi2, mi_a3]

        # If idle, and action a1 attacks 0, -1  -1,0
    elif (a1 == '-') and s == '-1' and (addr2 > addr1) and action_idle_attack == 0:  # and action_swap_1_2 == -1:
        idle = '-1'
        m = mi

        i, a1, violation, start_time1, mi1, mi_a2 = \
            pep_action_a(a1, m, i, ma1, ma2, ma3, count_coord, lines_cp_coord, lines_attack_coord, addrx, idle, m_max,
                         addr1, addr2)

        if violation == 'Not_exceeded':
            violation = 'feasible'
            mem_violation = 1
        else:
            violation = 'Infeasible'
            mem_violation = 0
        swap_pos = int(lines_attack_coord[addrx].split()[0])
        a_1 = a1
        idle = '-' + str(swap_pos)
        attack_swap = [i, start_time, swap_pos, s, a_1, 'N/A', 'N/A', idle, mi, violation, mem_violation, start_time1,
                       mi1, mi_a2, 'N/A']

        # idle, and action a2 attacks  1,-1
    elif (a2 == '-') and s == '-1' and (addr2 > addr1) and action_idle_attack == 1:
        idle = '-1'
        m = mi

        i, a2, violation, start_time1, mi1, mi_a2 = \
            pep_action_a(a2, m, i, ma1, ma2, ma3, count_coord, lines_cp_coord, lines_attack_coord, addrx, idle, m_max,
                         addr1, addr2)

        if violation == 'Not_exceeded':
            violation = 'feasible'
            mem_violation = 1
        else:
            violation = 'Infeasible'
            mem_violation = 0
        swap_pos = int(lines_attack_coord[addrx].split()[0])
        a_2 = a2
        idle = '-' + str(swap_pos)
        attack_swap = [i, start_time, swap_pos, s, 'N/A', a_2, 'N/A', idle, mi, violation, mem_violation, start_time1,
                       mi1, mi_a2, 'N/A']


    elif (a3 == '-') and s == '-1' and (addr2 > addr1) and action_idle_attack == 2:
        idle = '-1'
        m = mi

        i, a3, violation, start_time1, mi1, mi_a2 = \
            pep_action_a(a3, m, i, ma1, ma2, ma3, count_coord, lines_cp_coord, lines_attack_coord, addrx, idle, m_max,
                         addr1, addr2)

        if violation == 'Not_exceeded':
            violation = 'feasible'
            mem_violation = 1
        else:
            violation = 'Infeasible'
            mem_violation = 0
        swap_pos = int(lines_attack_coord[addrx].split()[0])
        a_3 = a3
        idle = '-' + str(swap_pos)
        attack_swap = [i, start_time, swap_pos, s, 'N/A', 'N/A', a_3, idle, mi, violation, mem_violation, start_time1,
                       mi1, mi_a2, 'N/A']

    else:

        swap_pos = int(lines_attack_coord[addrx].split()[0])
        violation = 'Infeasible'
        mem_violation = 0

        attack_swap = [i, start_time, swap_pos, s, 'N/A', 'N/A', 'N/A', 'N/A', mi, violation, mem_violation, start_time,
                       'N/A', 'N/A', 'N/A']

    return attack_swap
