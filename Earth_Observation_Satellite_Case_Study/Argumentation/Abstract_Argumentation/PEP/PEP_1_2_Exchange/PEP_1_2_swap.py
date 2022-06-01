import numpy as np
import pandas as pd
from Earth_Observation_Satellite_Case_Study.Argumentation.Abstract_Argumentation.PEP.PEP_calc import PEP_action_a

day = 3
filename1 = '../../PEP_Results/Day/PEP_1_2_Swap/Attack_swap_a1_2' + str(day) + '.txt'

# load of attacks summary information
attack_path = '../../SEP_Results/Day/Argumentation' + str(day) + '.txt'
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


solver_path = '../../SEP_Results/Day/Optimized_results' + str(day) + '.txt'
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
attack_swap1_2 = [['i', 'start_time','swap_location', 'S', 'a1','a2','mi', 'violation','mem_vio', 'time_of_incident', 'mem1','mem2']]

# file1 = open(filename1, 'w')
# file1.close()
# #attack_swap1_2=[]

def PEP_1_2_Swap(datastart, dataend, x1, addr1, y1, addr2):
#def PEP_1_2_Swap(datastart, dataend,pic_strt,pic_addr,proc_strt,proc_addr):


    if addr1<addr2:
        start_point = datastart+ addr1
        i = start_point
        s = ('addr1')
        start_time = int(lines_attack_coord[i].split()[0])
    else:
        start_point = datastart + addr2
        i = start_point
        s = ('addr2')
        start_time = int(lines_attack_coord[i].split()[0])

    print(s,dataend,start_point,i+1, start_time)
    #print()
    #while i in range( start_point, start_point+1):
        # print('restart')
    attack_data = lines_attack_coord[i].split()
    #start_time = int(attack_data[0])
    #end_time = start_time + time_interval
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

    #print(S, a1,a2)
    # mi_a1 = m1
    if (a1 == '-') and S =='1'and (addr2 > addr1):
        a_2 ='1'
        i, a1, violation, start_time1, mi1, mi_a2 = \
            PEP_action_a(a1, m1, i, ma1, ma2, ma3,count_coord,lines_cp_coord,lines_attack_coord,S,a_2,m_max,addr1,addr2)
        if violation == 'Not_exceeded':
            violation = 'feasible'
            mem_violation = 1
        else:
            violation = 'Infeasible'
            mem_violation = 0
        swap_pos = x1
        a_1 =a1
        a_2 = '-' + str(swap_pos)

        attack_swap1_2.append([i, start_time,swap_pos, S, a_1, a_2, mi,  violation, mem_violation, start_time1, mi1, mi_a2])
        print(['1st',i, start_time,swap_pos, S, a_1, a_2, mi, violation, mem_violation, start_time1, mi1, mi_a2])
        # file1 = open(filename1, 'a')
        # file1.write("\n")
        # df = pd.DataFrame([attack_swap1_2[len(attack_swap1_2) - 1]])
        # # file1.write("\n")
        # file1.writelines(df.to_string(header=False, index=False))

    elif (a2 == '-') and S =='0' and (addr2 > addr1):
        a_2 = '0'
        i, a1, violation, start_time1, mi1,mi_a2 = \
            PEP_action_a(a2, m2, i, ma1, ma2, ma3, count_coord, lines_cp_coord, lines_attack_coord, S, a_2, m_max,addr1,addr2)
        if violation == 'Not_exceeded':
            violation = 'feasible'
            mem_violation = 1
        else:
            violation = 'Infeasible'
            mem_violation = 0
        swap_pos = y1
        a_1 = '-' + str(swap_pos)
        a_2 = '-'

        attack_swap1_2.append([i, start_time,swap_pos, S, a_1, a_2, mi, violation, mem_violation, start_time1, mi1, mi_a2])
        print(['2nd',i, start_time,swap_pos, S, a_1, a_2, mi, violation, mem_violation, start_time1, mi1, mi_a2])
        # file1 = open(filename1, 'a')
        # file1.write("\n")
        # df = pd.DataFrame([attack_swap1_2[len(attack_swap1_2) - 1]])
        # # file1.write("\n")
        # file1.writelines(df.to_string(header=False, index=False))

    #
    # elif (a1 == '-') and S =='1'and (addr1 > addr2):
    #     a_2 ='1'
    #     i, a1, violation, start_time1, mi1, mi_a2 = \
    #         PEP_action_a(a1, m1, i, ma1, ma2, ma3,count_coord,lines_cp_coord,lines_attack_coord,S,a_2,m_max,addr2,addr1)
    #     if violation == 'Not_exceeded':
    #         violation = 'feasible'
    #         mem_violation = 1
    #     else:
    #         violation = 'Infeasible'
    #         mem_violation = 0
    #     swap_pos = y1
    #     a_1 =a1
    #     a_2 = '-' + str(swap_pos)
    #     swap_pos = x1
    #     attack_swap1_2.append([i, start_time,swap_pos, S, a_1, a_2, mi,  violation, mem_violation, start_time1, mi1, mi_a2])
    #     print(['1st',i, start_time,swap_pos, S, a_1, a_2, mi, violation, mem_violation, start_time1, mi1, mi_a2])
    #     # file1 = open(filename1, 'a')
    #     # file1.write("\n")
    #     # df = pd.DataFrame([attack_swap1_2[len(attack_swap1_2) - 1]])
    #     # # file1.write("\n")
    #     # file1.writelines(df.to_string(header=False, index=False))
    #
    # elif (a2 == '-') and S =='0' and (addr1 > addr2):
    #     a_2 = '0'
    #     i, a1, violation, start_time1, mi1,mi_a2 = \
    #         PEP_action_a(a2, m2, i, ma1, ma2, ma3, count_coord, lines_cp_coord, lines_attack_coord, S, a_2, m_max,addr2,addr1)
    #     if violation == 'Not_exceeded':
    #         violation = 'feasible'
    #         mem_violation = 1
    #     else:
    #         violation = 'Infeasible'
    #         mem_violation = 0
    #     swap_pos = x1
    #     a_1 = '-' + str(swap_pos)
    #     a_2 = '-'
    #     start_time = y1
    #     attack_swap1_2.append([i, start_time,swap_pos, S, a_1, a_2, mi, violation, mem_violation, start_time1, mi1, mi_a2])
    #     print(['2nd',i, start_time,swap_pos, S, a_1, a_2, mi, violation, mem_violation, start_time1, mi1, mi_a2])
        # file1 = open(filename1, 'a')
    elif (a1 != '-') or (a2 != '-'):
        if (a1 != '-') and S =='1' and (addr2>addr1):
            swap_pos = y1
        elif (a1 != '-') and S =='1' and (addr1>addr2):
            swap_pos = x1
        elif (a1 != '-') and S =='0' and (addr2>addr1):
            swap_pos = y1
        else:#if (a1 != '-') and S =='0' and (addr1>addr2):
            swap_pos = x1
        violation = 'Infeasible'
        mem_violation = 0
        attack_swap1_2.append([i, start_time, swap_pos, S, 'N/A', 'N/A', mi, violation, mem_violation, start_time, 'N/A', 'N/A'])
        print(['null', i, start_time, swap_pos, S,'N/A', 'N/A', mi, violation, mem_violation, start_time, 'N/A', 'N/A'])


        #i = i + 1

    #return mem_violation
    return attack_swap1_2



x=[]
y=[]
x_action = []
y_action = []

datastart = 15000
#dataend = count_attack_coord-2270
dataend = count_attack_coord-2100

#Extract all matching data for times of action execution and action execution itself
for i in range(datastart, dataend):
    x_y_data = lines_attack_coord[i].split()
    x_time = int(x_y_data[0])
    y_time = int(x_y_data[0])
    S_x_data = int(x_y_data[4])
    S_y_data =  int(x_y_data[4])

    mi = x_y_data[5]

    x.append(x_time)
    y.append(y_time)
    x_action.append(S_x_data)
    y_action.append(S_y_data)


x1_coordinates=[]
y1_coordinates=[]
mem_violation =[]
final_list =[]

for i in range(len(x) - 1):
    for j in range(len(y) - 1):
        print(i,j,x_action[i], y_action[j])
        if  [x_action[i], y_action[j]] == [0, 1]:
            x1 = x[i]
            y1 = y[j]
            addr1 = i
            addr2 = j
            print('0,1', x1, addr1,':', y1, addr2)

            final_list = PEP_1_2_Swap(datastart, dataend, x1, addr1, y1, addr2)
            #print(attack_swap)
        elif [x_action[i], y_action[j]] == [1, 0]:
            x1 = x[i]
            y1 = y[j]
            addr1 = i
            addr2 = j
            # proc_addr = i
            # pic_addr = j

            print('1, 0', x1, addr1,':', y1, addr2)
            #attack_swap = PEP_1_2_Swap(datastart, dataend, x1, pic_addr, y1, proc_addr)
            final_list = PEP_1_2_Swap(datastart, dataend, x1, addr1, y1, addr2)

        else:
            x1 = x_action[i]
            y1 = y_action[j]
            mem_vio =-1
        x1_coordinates.append(x1)
        y1_coordinates.append(y1)
        #mem_violation.append(mem_vio)


file1 = open(filename1, 'w')
#file1.write("\n")
df = pd.DataFrame(final_list)
# file1.write("\n")
file1.writelines(df.to_string(header=False, index=False))