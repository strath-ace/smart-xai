# PEP calculation 1 used to initiate swapping between actions

import pandas as pd

from Earth_Observation_Satellite_Case_Study.Argumentation.Abstract_Argumentation.PEP.PEP_Feasible_check import PEP_check_Swap

day = 3
filename1 = '../PEP_Results/Day/PEP_1_2_Swap/Attack_swap_a' + str(day) + '.txt'

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



x=[]
y=[]
x_action = []
y_action = []

datastart = 1
dataend = count_attack_coord-1

#datastart = 15000
#dataend = count_attack_coord-2270
#dataend = count_attack_coord-2100

# Extract all matching data for times of action execution and action execution itself
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
file1 = open(filename1, 'w')
final_list =[['i', 'start_time','swap_location', 'S', 'a1','a2','a3', 'idle', 'mi', 'violation','mem_vio', 'time_of_incident', 'mem1','mem2','mem3']]

# Create an (n x m) matrix with each action scheduled and check if they both can be swapped once they aren't the same action
# Meaning can any 2 actions be swapped?
# rows
for i in range(len(x) - 1):
    # initialize list
    if i > 0:
        final_list = []

    # columns
    for j in range(len(y) - 1):

      # print(i,j,x_action[i], y_action[j])
        action_swap1 = x_action[i]
        action_swap2 = y_action[j]

      # first 2 if statements to exchange processing with images taken
        if  [x_action[i], y_action[j]] == [0, 1]:
            x1 = x[i]
            y1 = y[j]
            addr1 = i
            addr2 = j
          # print('0,1', x1, addr1,':', y1, addr2)
            final_list.append(PEP_check_Swap(datastart, dataend, x1, addr1, y1, addr2, action_swap1, action_swap2))
            #final_list = PEP_check_Swap(datastart, dataend, x1, addr1, y1, addr2,action_swap1,action_swap2)
            #print(attack_swap)
        elif [x_action[i], y_action[j]] == [1, 0]:
            x1 = x[i]
            y1 = y[j]
            addr1 = i
            addr2 = j

          # print('1, 0', x1, addr1,':', y1, addr2)
            final_list.append(PEP_check_Swap(datastart, dataend, x1, addr1, y1, addr2, action_swap1, action_swap2))
            #final_list = PEP_check_Swap(datastart, dataend, x1, addr1, y1, addr2,action_swap1,action_swap2)
        # The next 2 if statements are swapping image taking with idle time
        elif [x_action[i], y_action[j]] == [0, -1]:
            x1 = x[i]
            y1 = y[j]
            addr1 = i
            addr2 = j
          # print('0,-1', x1, addr1, ':', y1, addr2)
            final_list.append(PEP_check_Swap(datastart, dataend, x1, addr1, y1, addr2, action_swap1, action_swap2))
            #final_list = PEP_check_Swap(datastart, dataend, x1, addr1, y1, addr2,action_swap1,action_swap2)
            # print(attack_swap)
        elif [x_action[i], y_action[j]] == [-1, 0]:
            x1 = x[i]
            y1 = y[j]
            addr1 = i
            addr2 = j

            # print('-1, 0', x1, addr1, ':', y1, addr2)
            final_list.append(PEP_check_Swap(datastart, dataend, x1, addr1, y1, addr2, action_swap1, action_swap2))
            # final_list = PEP_check_Swap(datastart, dataend, x1, addr1, y1, addr2,action_swap1,action_swap2)
        # The next 2 if statements are swapping with image taking and down-linking
        elif [x_action[i], y_action[j]] == [0, 2]:
            x1 = x[i]
            y1 = y[j]
            addr1 = i
            addr2 = j
          # print('0,2', x1, addr1, ':', y1, addr2)
            final_list.append(PEP_check_Swap(datastart, dataend, x1, addr1, y1, addr2, action_swap1, action_swap2))
            #final_list = PEP_check_Swap(datastart, dataend, x1, addr1, y1, addr2,action_swap1,action_swap2)
            # print(attack_swap)
        elif [x_action[i], y_action[j]] == [2, 0]:
            x1 = x[i]
            y1 = y[j]
            addr1 = i
            addr2 = j

          # print('2, 0', x1, addr1, ':', y1, addr2)
            final_list.append(PEP_check_Swap(datastart, dataend, x1, addr1, y1, addr2, action_swap1, action_swap2))
            #final_list = PEP_check_Swap(datastart, dataend, x1, addr1, y1, addr2,action_swap1,action_swap2)
        # The next 2 if statements are swapping with image taking and idle time
        elif [x_action[i], y_action[j]] == [1, -1]:
            x1 = x[i]
            y1 = y[j]
            addr1 = i
            addr2 = j
          # print('0,-1', x1, addr1, ':', y1, addr2)
            final_list.append(PEP_check_Swap(datastart, dataend, x1, addr1, y1, addr2, action_swap1, action_swap2))
            #final_list = PEP_check_Swap(datastart, dataend, x1, addr1, y1, addr2,action_swap1,action_swap2)
            # print(attack_swap)

        elif [x_action[i], y_action[j]] == [-1, 1]:
            x1 = x[i]
            y1 = y[j]
            addr1 = i
            addr2 = j

            # print('-1, 0', x1, addr1, ':', y1, addr2)
            final_list.append(PEP_check_Swap(datastart, dataend, x1, addr1, y1, addr2, action_swap1, action_swap2))
            # final_list = PEP_check_Swap(datastart, dataend, x1, addr1, y1, addr2,action_swap1,action_swap2)

        # The next 2 statements are swapping with actions process and down-link
        elif [x_action[i], y_action[j]] == [1, 2]:
            x1 = x[i]
            y1 = y[j]
            addr1 = i
            addr2 = j
            #print('1, 2', x1, addr1, ':', y1, addr2)
            final_list.append(PEP_check_Swap(datastart, dataend, x1, addr1, y1, addr2, action_swap1, action_swap2))
            #final_list = PEP_check_Swap(datastart, dataend, x1, addr1, y1, addr2,action_swap1,action_swap2)
            # print(attack_swap)

        elif [x_action[i], y_action[j]] == [2, 1]:
            x1 = x[i]
            y1 = y[j]
            addr1 = i
            addr2 = j

            #print('2, 1', x1, addr1, ':', y1, addr2)
            final_list.append(PEP_check_Swap(datastart, dataend, x1, addr1, y1, addr2, action_swap1, action_swap2))
            #final_list = PEP_check_Swap(datastart, dataend, x1, addr1, y1, addr2,action_swap1,action_swap2)

        # The next 2 if statements are swapping with idle time with downlink
        elif [x_action[i], y_action[j]] == [2, -1]:
            x1 = x[i]
            y1 = y[j]
            addr1 = i
            addr2 = j
            #print('1, 2', x1, addr1, ':', y1, addr2)
            final_list.append(PEP_check_Swap(datastart, dataend, x1, addr1, y1, addr2, action_swap1, action_swap2))
            #final_list = PEP_check_Swap(datastart, dataend, x1, addr1, y1, addr2,action_swap1,action_swap2)
            # print(attack_swap)
        elif [x_action[i], y_action[j]] == [-1, 2]:
            x1 = x[i]
            y1 = y[j]
            addr1 = i
            addr2 = j

            #print('2, 1', x1, addr1, ':', y1, addr2)
            final_list.append(PEP_check_Swap(datastart, dataend, x1, addr1, y1, addr2, action_swap1, action_swap2))
            #final_list = PEP_check_Swap(datastart, dataend, x1, addr1, y1, addr2,action_swap1,action_swap2)

        else:
            x1 = x_action[i]
            y1 = y_action[j]
            mem_vio =-1
        x1_coordinates.append(x1)
        y1_coordinates.append(y1)
        #mem_violation.append(mem_vio)
  # print(len(final_list),final_list[1])
    if final_list[0][0]=='i' and len(final_list)>0:
      # print('start')
        file1 = open(filename1, 'a')
        #file1.write("\n")
        df = pd.DataFrame(final_list)
        #file1.write("\n")
        file1.writelines(df.to_string(header=False, index=False))
    else:
        file1 = open(filename1, 'a')
        file1.write("\n")
        df = pd.DataFrame(final_list)
        #file1.write("\n")
        file1.writelines(df.to_string(header=False, index=False))

