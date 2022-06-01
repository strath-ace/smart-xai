# PEP calculation 2

from Earth_Observation_Satellite_Case_Study.Argumentation.Abstract_Argumentation.PEP.PEP_calc import PEP_action_a


day = 3
# load of attacks summary information
attack_path = '../SEP_Results/Day/Argumentation' + str(day) + '.txt'
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


solver_path = '../SEP_Results/Day/Optimized_results' + str(day) + '.txt'
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



time_interval = 5
# onboard memory is 80% of total memory 2TB - 1,920,000
onboard_mem = int(0.8 * 24 * 10 ** 5)
#  memory required per image
image_mem = 2688
# downlink data rate
downlink_data_rate = 280 * 2 * time_interval
# 5000Kbit/s to process images
process_im_mem = 50 * time_interval

#attack_swap = [['i', 'start_time','swap_location', 'S', 'a1','a2','a3','mi', 'violation','mem_vio', 'time_of_incident', 'mem1','mem2','mem3']]
#attack_swap = []

def PEP_check_Swap(datastart, dataend, x1, addr1, y1, addr2, action_swap1, action_swap2):
#def PEP_1_2_Swap(datastart, dataend,pic_strt,pic_addr,proc_strt,proc_addr):
    #attack_swap = [['i', 'start_time','swap_location', 'S', 'a1','a2','a3','mi', 'violation','mem_vio', 'time_of_incident', 'mem1','mem2','mem3']]
    # if addr1 > datastart :
    attack_swap = []
    #else:
       # attack_swap = [['i', 'start_time', 'swap_location', 'S', 'a1', 'a2', 'a3', 'mi', 'violation', 'mem_vio', 'time_of_incident', 'mem1', 'mem2', 'mem3']]

    if addr1 < addr2:
        start_point = datastart + addr1
        i = start_point
        s = ('addr1')
        start_time = int(lines_attack_coord[i].split()[0])
        addrx = datastart + addr2
    else:
        start_point = datastart + addr2
        i = start_point
        s = ('addr2')
        start_time = int(lines_attack_coord[i].split()[0])
        addrx = datastart + addr1

    action_idle_attack = 5
    action_swap_1_2 = -1
    if (action_swap2 == -1 or action_swap1 == -1):
        if [action_swap1, action_swap2] == [0,-1] or [action_swap1, action_swap2]==[-1,0]:
            action_idle_attack = 0
        elif [action_swap1, action_swap2] == [1,-1] or [action_swap1, action_swap2] == [-1,1]:
            action_idle_attack = 1
        elif [action_swap1, action_swap2] == [2,-1] or [action_swap1, action_swap2] == [-1,2]:
            action_idle_attack = 2

    else:
        if [action_swap1, action_swap2] == [0,1] or [action_swap1, action_swap2] == [1,0]:
            action_swap_1_2 = 0
        elif [action_swap1, action_swap2] == [0,2] or [action_swap1, action_swap2] == [2,0]:
            action_swap_1_2 = 1
        elif [action_swap1, action_swap2] == [1,2] or [action_swap1, action_swap2] == [2,1]:
            action_swap_1_2 = 2



  # print(addrx,int(lines_attack_coord[addrx].split()[0]))

  # print(s,dataend,start_point,i+1, start_time,'actions',action_swap1, action_swap2,addr1,addr2)

    attack_data = lines_attack_coord[i].split()

    # land = attack_data[1]
    # station = attack_data[2]
    # day = attack_data[3]
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
    idle = 'N/A'

    #print(S, a1,a2)
    # action attack with a1 and a2 0,1   1,0
    if (a1 == '-') and S =='1'and (addr2 > addr1) and (action_swap_1_2 == 0):
        a_2 ='1'
        i, a1, violation, start_time1, mi1, mi_a2 = \
            PEP_action_a(a1, m1, i, ma1, ma2, ma3,count_coord,lines_cp_coord,lines_attack_coord,addrx,a_2,m_max,addr1,addr2)
        if violation == 'Not_exceeded':
            violation = 'feasible'
            mem_violation = 1
        else:
            violation = 'Infeasible'
            mem_violation = 0
        swap_pos = int(lines_attack_coord[addrx].split()[0])
        a_1 =a1
        a_2 = '-' + str(swap_pos)
        attack_swap=[i, start_time, swap_pos, S, a_1, a_2, 'N/A', idle, mi, violation, mem_violation, start_time1, mi1, mi_a2, 'N/A']
        #attack_swap.append([i, start_time,swap_pos, S, a_1, a_2,'N/A', mi,  violation, mem_violation, start_time1, mi1, mi_a2,'N/A'])
      # print(['a1_a2_1st',i, start_time,swap_pos, S, a_1, a_2,'N/A',idle, mi, violation, mem_violation, start_time1, mi1, mi_a2,'N/A'])

    elif (a2 == '-') and S =='0' and (addr2 > addr1) and (action_swap_1_2 == 0) :
        a_2 = '0'
        i, a2, violation, start_time1, mi1,mi_a2 = \
            PEP_action_a(a2, m2, i, ma1, ma2, ma3, count_coord, lines_cp_coord, lines_attack_coord, addrx, a_2, m_max,addr1,addr2)
        if violation == 'Not_exceeded':
            violation = 'feasible'
            mem_violation = 1
        else:
            violation = 'Infeasible'
            mem_violation = 0
        swap_pos = int(lines_attack_coord[addrx].split()[0])
        a_1 = '-' + str(swap_pos)
        a_2 = a2
        attack_swap = [i, start_time, swap_pos, S, a_1, a_2, 'N/A',idle, mi, violation, mem_violation, start_time1, mi1, mi_a2, 'N/A']
        #attack_swap.append([i, start_time,swap_pos, S, a_1, a_2,'N/A', mi, violation, mem_violation, start_time1, mi1, mi_a2,'N/A'])
      # print(['a1_a2_2nd',i, start_time,swap_pos, S, a_1, a_2,'N/A',idle, mi, violation, mem_violation, start_time1, mi1, mi_a2,'N/A'])

    # a1 attack a3 for swap  2,0
    elif (a1 == '-') and S =='2'and (addr2 > addr1)  and (action_swap_1_2 == 1):
        a_3 ='2'
        i, a1, violation, start_time1, mi1, mi_a3 = \
            PEP_action_a(a1, m1, i, ma1, ma2, ma3,count_coord,lines_cp_coord,lines_attack_coord,addrx,a_3,m_max,addr1,addr2)
        if violation == 'Not_exceeded':
            violation = 'feasible'
            mem_violation = 1
        else:
            violation = 'Infeasible'
            mem_violation = 0
        swap_pos = int(lines_attack_coord[addrx].split()[0])
        a_1 =a1
        a_3 = '-' + str(swap_pos)
        attack_swap = [i, start_time,swap_pos, S, a_1,'N/A', a_3, idle, mi, violation, mem_violation, start_time1, mi1,'N/A', mi_a3]
        #attack_swap.append([i, start_time,swap_pos, S, a_1,'N/A', a_3, mi,  violation, mem_violation, start_time1, mi1,'N/A', mi_a3])
      # print(['a1_a3_1st',i, start_time,swap_pos, S, a_1,'N/A', a_3, mi, idle, violation, mem_violation, start_time1, mi1,'N/A', mi_a3])

    # 0,2
    elif (a3 == '-') and S =='0' and (addr2 > addr1)  and (action_swap_1_2 == 1):
        a_3 = '0'
        i, a3, violation, start_time1, mi1, mi_a3 = \
            PEP_action_a(a3, m3, i, ma1, ma2, ma3, count_coord, lines_cp_coord, lines_attack_coord, addrx, a_3, m_max,addr1,addr2)
        if violation == 'Not_exceeded':
            violation = 'feasible'
            mem_violation = 1
        else:
            violation = 'Infeasible'
            mem_violation = 0
        swap_pos = int(lines_attack_coord[addrx].split()[0])
        a_1 = '-' + str(swap_pos)
        a_3 = a3
        attack_swap = [i, start_time,swap_pos, S, a_1,'N/A', a_3, idle, mi, violation, mem_violation, start_time1, mi1,'N/A', mi_a3]
        #attack_swap.append([i, start_time,swap_pos, S, a_1,'N/A', a_3, mi, violation, mem_violation, start_time1, mi1,'N/A', mi_a3])
      # print(['a1_a3_2nd',i, start_time,swap_pos, S, a_1,'N/A', a_3, idle, mi, violation, mem_violation, start_time1, mi1,'N/A', mi_a3])

    # a2 attack a3 for swap  2,1
    elif (a2 == '-') and S == '2' and (addr2 > addr1)  and (action_swap_1_2 == 2):
        a_3 = '2'
        i, a2, violation, start_time1, mi2, mi_a3 = \
            PEP_action_a(a2, m2, i, ma1, ma2, ma3, count_coord, lines_cp_coord, lines_attack_coord, addrx, a_3, m_max, addr1, addr2)
        if violation == 'Not_exceeded':
            violation = 'feasible'
            mem_violation = 1
        else:
            violation = 'Infeasible'
            mem_violation = 0
        swap_pos = int(lines_attack_coord[addrx].split()[0])
        a_2 = a2
        a_3 = '-' + str(swap_pos)
        attack_swap = [i, start_time, swap_pos, S,'N/A', a_2, a_3, idle, mi, violation, mem_violation, start_time1,'N/A', mi2, mi_a3]
        #attack_swap.append([i, start_time, swap_pos, S,'N/A', a_2, a_3, mi, violation, mem_violation, start_time1,'N/A', mi2, mi_a3])
      # print(['a2_a3_1st', i, start_time, swap_pos, S,'N/A', a_2, a_3, idle, mi, violation, mem_violation, start_time1,'N/A', mi2, mi_a3])

    # 1,2
    elif (a3 == '-') and S == '1' and (addr2 > addr1)  and (action_swap_1_2 == 2):
        a_3 = '1'
        i, a3, violation, start_time1, mi2, mi_a3 = \
            PEP_action_a(a3, m3, i, ma1, ma2, ma3, count_coord, lines_cp_coord, lines_attack_coord, addrx, a_3, m_max, addr1, addr2)
        if violation == 'Not_exceeded':
            violation = 'feasible'
            mem_violation = 1
        else:
            violation = 'Infeasible'
            mem_violation = 0
        swap_pos = int(lines_attack_coord[addrx].split()[0])
        a_2 = '-' + str(swap_pos)
        a_3 = a3
        attack_swap=[i, start_time, swap_pos, S,'N/A', a_2, a_3, idle, mi, violation, mem_violation, start_time1,'N/A', mi2, mi_a3]
        #attack_swap.append([i, start_time, swap_pos, S,'N/A', a_2, a_3, mi, violation, mem_violation, start_time1,'N/A', mi2, mi_a3])
      # print(['a2_a3_2nd', i, start_time, swap_pos, S,'N/A', a_2, a_3, idle, mi, violation, mem_violation, start_time1,'N/A', mi2, mi_a3])

        # If idle, and action a1 attacks 0, -1  -1,0
    elif (a1 == '-') and S == '-1' and (addr2 > addr1) and action_idle_attack == 0:  # and action_swap_1_2 == -1:
        idle = '-1'
        m = mi

        i, a1, violation, start_time1, mi1, mi_a2 = \
            PEP_action_a(a1, m, i, ma1, ma2, ma3, count_coord, lines_cp_coord, lines_attack_coord, addrx, idle, m_max, addr1, addr2)

        if violation == 'Not_exceeded':
            violation = 'feasible'
            mem_violation = 1
        else:
            violation = 'Infeasible'
            mem_violation = 0
        swap_pos = int(lines_attack_coord[addrx].split()[0])
        a_1 = a1
        idle = '-' + str(swap_pos)
        attack_swap=[i, start_time, swap_pos, S, a_1, 'N/A', 'N/A', idle, mi, violation, mem_violation, start_time1, mi1, mi_a2, 'N/A']
        #attack_swap.append([i, start_time, swap_pos, S, a_1, a_2, 'N/A', mi, violation, mem_violation, start_time1, mi1, mi_a2, 'N/A'])
      # print(['idle_a1_1st', i, start_time, swap_pos, S, a_1,'N/A', 'N/A', idle, mi, violation, mem_violation, start_time1, mi1, mi_a2, 'N/A'])

        # idle, and action a2 attacks  1,-1
    elif (a2 == '-') and S == '-1' and (addr2 > addr1) and action_idle_attack == 1:
        idle = '-1'
        m = mi

        i, a2, violation, start_time1, mi1, mi_a2 = \
                PEP_action_a(a2, m, i, ma1, ma2, ma3, count_coord, lines_cp_coord, lines_attack_coord, addrx, idle, m_max, addr1, addr2)

        if violation == 'Not_exceeded':
            violation = 'feasible'
            mem_violation = 1
        else:
            violation = 'Infeasible'
            mem_violation = 0
        swap_pos = int(lines_attack_coord[addrx].split()[0])
        a_2 = a2
        idle = '-' + str(swap_pos)
        attack_swap=[i, start_time, swap_pos, S, 'N/A', a_2, 'N/A', idle, mi, violation, mem_violation, start_time1, mi1, mi_a2, 'N/A']
        #attack_swap.append([i, start_time, swap_pos, S, a_1, a_2, 'N/A', mi, violation, mem_violation, start_time1, mi1, mi_a2, 'N/A'])
      # print(['idle_a2_1st', i, start_time, swap_pos, S,'N/A', a_2, 'N/A', idle, mi, violation, mem_violation, start_time1, mi1, mi_a2, 'N/A'])

    elif (a3 == '-') and S == '-1' and (addr2 > addr1) and action_idle_attack == 2:
        idle = '-1'
        m = mi

        i, a3, violation, start_time1, mi1, mi_a2 = \
                PEP_action_a(a3, m, i, ma1, ma2, ma3, count_coord, lines_cp_coord, lines_attack_coord, addrx, idle, m_max, addr1, addr2)

        if violation == 'Not_exceeded':
            violation = 'feasible'
            mem_violation = 1
        else:
            violation = 'Infeasible'
            mem_violation = 0
        swap_pos = int(lines_attack_coord[addrx].split()[0])
        a_3 = a3
        idle = '-' + str(swap_pos)
        attack_swap=[i, start_time, swap_pos, S, 'N/A','N/A', a_3 ,idle, mi, violation, mem_violation, start_time1, mi1, mi_a2, 'N/A']
        #attack_swap.append([i, start_time, swap_pos, S, a_1, a_2, 'N/A', mi, violation, mem_violation, start_time1, mi1, mi_a2, 'N/A'])
      # print(['idle_a2_1st', i, start_time, swap_pos, S, 'N/A','N/A', a_3 ,idle, mi, violation, mem_violation, start_time1, mi1, mi_a2, 'N/A'])

    # elif (a1 != '-') or (a2 != '-') or (a3 != '-'):
    #     # a1 (S=0) vs a2 (S=1)
    #     if (a1 != '-') and S =='1' and (addr2>addr1):
    #         swap_pos = int(lines_attack_coord[addrx].split()[0])
    #     elif (a1 != '-') and S =='1' and (addr1>addr2):
    #         swap_pos = int(lines_attack_coord[addrx].split()[0])
    #     elif (a1 != '-') and S =='0' and (addr2>addr1):
    #         swap_pos = int(lines_attack_coord[addrx].split()[0])
    #     # a1 (S=0) vs a3 (S=2)
    #     elif (a1 != '-') and S =='2' and (addr2>addr1):
    #         swap_pos = int(lines_attack_coord[addrx].split()[0])
    #     elif (a1 != '-') and S =='2' and (addr1>addr2):
    #         swap_pos = int(lines_attack_coord[addrx].split()[0])
    #     # a2 (S=1) vs a3 (S=2)
    #     elif (a2 != '-') and S == '2' and (addr2 > addr1):
    #         swap_pos = int(lines_attack_coord[addrx].split()[0])
    #     elif (a2 != '-') and S == '2' and (addr1 > addr2):
    #         swap_pos = int(lines_attack_coord[addrx].split()[0])
    #     elif (a2 != '-') and S =='1' and (addr2>addr1):
    #         swap_pos = int(lines_attack_coord[addrx].split()[0])
    else:
        #if (addr2>addr1):
            swap_pos = int(lines_attack_coord[addrx].split()[0])
            violation = 'Infeasible'
            mem_violation = 0


            attack_swap=[i, start_time, swap_pos, S, 'N/A', 'N/A', 'N/A','N/A', mi, violation, mem_violation, start_time, 'N/A', 'N/A', 'N/A']
   # attack_swap.append([i, start_time, swap_pos, S, 'N/A', 'N/A','N/A', mi, violation, mem_violation, start_time,'N/A', 'N/A', 'N/A'])
        #print(['null', i, start_time, swap_pos, S,'N/A', 'N/A','N/A', mi, violation, mem_violation, start_time,'N/A', 'N/A', 'N/A'])


        #i = i + 1

    #return mem_violation
    return attack_swap