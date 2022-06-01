#PEP calculation 4

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.colors import ListedColormap


day = 3
filename = '../../PEP_Results/Day/PEP_1_2_Swap/Attack_summary_a' + str(day) + '.txt'

# load of attacks summary information
attack_path_0_1 = '../../PEP_Results/Day/PEP_1_2_Swap/Attack_swap_a' + str(day) + '.txt'
attack_coord_0_1 = open(attack_path_0_1, "r")
count_attack_coord_0_1 = 0
# for loop to count the number of lines in file
for line in attack_coord_0_1:
    if line != "\n":
        count_attack_coord_0_1 += 1
attack_coord_0_1.close()
print(count_attack_coord_0_1)
# load data line by line
attack_coord_0_1 = open(attack_path_0_1, "r")
attack_cp_coord_0_1 = attack_coord_0_1.read()
lines_attack_coord_0_1 = attack_cp_coord_0_1.split('\n')


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

datastart = 1
#dataend = 1604
#dataend = count_attack_coord-2270
dataend = count_attack_coord-2
min_number = int(lines_attack_coord[datastart].split()[0])
max_number = int(lines_attack_coord[dataend].split()[0])
print('min',min_number)
print('max',max_number)

grid_size = 5
x = np.arange(min_number, max_number+1, grid_size)
y = np.arange(min_number, max_number+1, grid_size)


x_coordinates = []
y_coordinates = []
for i in range(datastart, dataend):

    S_x_data = int(lines_attack_coord[i].split()[4])
    S_y_data = int(lines_attack_coord[i].split()[4])
    x_coordinates.append(S_x_data)
    y_coordinates.append(S_y_data)


swap_1_2_summary=[]
for n in range (1,count_attack_coord_0_1):
#for n in range (9275768-1,9275768+2):
    swap_1_2x = int(lines_attack_coord_0_1[n].split()[1])
    swap_1_2y = int(lines_attack_coord_0_1[n].split()[2])
    #print(n,lines_attack_coord_0_1[n].split())
    swap_1_2_vio = int(lines_attack_coord_0_1[n].split()[10])
    swap_1_2_summary.append([swap_1_2x,swap_1_2y,swap_1_2_vio])

file1 = open(filename, 'w')
#file1.write("\n")
df = pd.DataFrame(swap_1_2_summary)
# file1.write("\n")
file1.writelines(df.to_string(header=False, index=False))
print(len(swap_1_2_summary))


# create a colormap with two colors, vmin and vmax are chosen so that their center is the pivot value
cmap = ListedColormap(['indigo','red', 'gold'])


pivot_value = 1
#x_coordinates=[1,0,2,2,1,0,3,1]
x_coordinates=np.array(x_coordinates)
#y_coordinates=[1,0,2,2,1,0,3,1]

#print(x)
y_coordinates=np.array(y_coordinates)
# print(x_coordinates)
# print(y_coordinates)

x1_coordinates=[]
y1_coordinates=[]
vio_list =[]
#for i in range(len(x) - 2):
for i in range(1603):
    for j in range(len(y) - 2):
        vio = 0
        if  [x_coordinates[i], y_coordinates[j]] == [0, 1]:
            x1 = x[i]
            y1 = y[j]
            addr1 = i
            addr2 = j
            #print( x1, addr1,':', y1, addr2)
            #print('yes0')

            index =[(a, swap_add.index(x1))for a, swap_add in enumerate(swap_1_2_summary) if x1 in swap_add]
            index2 = [(a, swap_add.index(y1))for a, swap_add in enumerate(swap_1_2_summary) if y1 in swap_add]
            for v in range(len(index)-1):
                pos1 = index[v][0]
                vio1 = swap_1_2_summary[pos1][2]
                for v2 in range(len(index2)-1):
                    pos2 = index2[v2][0]
                    vio2 = swap_1_2_summary[pos2][2]
                    if pos1 == pos2:
                        vio = vio1
                        #y1 = vio
                        if vio == 1:
                            x1_coordinates.append(x1)
                            y1_coordinates.append(y1)
                    else:
                        vio = 0
                        #y1 = vio
                        #print(pos1)
            #print('index 1',index,'\nindex 2', index2)
        elif [x_coordinates[i], y_coordinates[j]] == [1, 0]:
            x1 = x[i]
            y1 = y[j]
            addr1 = i
            addr2 = j
            #print( x1, addr1,':', y1, addr2)

            #print('yes1')

            index =[(a, swap_add.index(x1))for a, swap_add in enumerate(swap_1_2_summary) if x1 in swap_add]
            index2 = [(a, swap_add.index(y1))for a, swap_add in enumerate(swap_1_2_summary) if y1 in swap_add]
            for v in range(0,len(index)-1):
                pos1 = index[v][0]
                vio1 = swap_1_2_summary[pos1][2]
                for v2 in range(0,len(index2)-1):
                    pos2 = index2[v2][0]
                    vio2 = swap_1_2_summary[pos2][2]
                    if pos1 == pos2:
                        vio = vio1
                        #y1 = vio
                        if vio == 1:
                            x1_coordinates.append(x1)
                            y1_coordinates.append(y1)
                    else:
                        vio = 0
                        #y1 = vio
                        #print(swap_1_2_summary[pos1])

        elif [x_coordinates[i], y_coordinates[j]] == [0, 2]:
            x1 = x[i]
            y1 = y[j]
            addr1 = i
            addr2 = j
            #print( x1, addr1,':', y1, addr2)

            #print('yes1')

            index =[(a, swap_add.index(x1))for a, swap_add in enumerate(swap_1_2_summary) if x1 in swap_add]
            index2 = [(a, swap_add.index(y1))for a, swap_add in enumerate(swap_1_2_summary) if y1 in swap_add]
            for v in range(0,len(index)-1):
                pos1 = index[v][0]
                vio1 = swap_1_2_summary[pos1][2]
                for v2 in range(0,len(index2)-1):
                    pos2 = index2[v2][0]
                    vio2 = swap_1_2_summary[pos2][2]
                    if pos1 == pos2:
                        vio = vio1
                        #y1 = vio
                        if vio == 1:
                            x1_coordinates.append(x1)
                            y1_coordinates.append(y1)
                    else:
                        vio = 0
        elif [x_coordinates[i], y_coordinates[j]] == [2, 0]:
            x1 = x[i]
            y1 = y[j]
            addr1 = i
            addr2 = j
            #print( x1, addr1,':', y1, addr2)

            #print('yes1')

            index =[(a, swap_add.index(x1))for a, swap_add in enumerate(swap_1_2_summary) if x1 in swap_add]
            index2 = [(a, swap_add.index(y1))for a, swap_add in enumerate(swap_1_2_summary) if y1 in swap_add]
            for v in range(0,len(index)-1):
                pos1 = index[v][0]
                vio1 = swap_1_2_summary[pos1][2]
                for v2 in range(0,len(index2)-1):
                    pos2 = index2[v2][0]
                    vio2 = swap_1_2_summary[pos2][2]
                    if pos1 == pos2:
                        vio = vio1
                        #y1 = vio
                        if vio == 1:
                            x1_coordinates.append(x1)
                            y1_coordinates.append(y1)
                    else:
                        vio = 0#

        elif [x_coordinates[i], y_coordinates[j]] == [1, 2]:
            x1 = x[i]
            y1 = y[j]
            addr1 = i
            addr2 = j
            #print( x1, addr1,':', y1, addr2)

            #print('yes1')

            index =[(a, swap_add.index(x1))for a, swap_add in enumerate(swap_1_2_summary) if x1 in swap_add]
            index2 = [(a, swap_add.index(y1))for a, swap_add in enumerate(swap_1_2_summary) if y1 in swap_add]
            for v in range(0,len(index)-1):
                pos1 = index[v][0]
                vio1 = swap_1_2_summary[pos1][2]
                for v2 in range(0,len(index2)-1):
                    pos2 = index2[v2][0]
                    vio2 = swap_1_2_summary[pos2][2]
                    if pos1 == pos2:
                        vio = vio1
                        #y1 = vio
                        if vio == 1:
                            x1_coordinates.append(x1)
                            y1_coordinates.append(y1)
                    else:
                        vio = 0
        elif [x_coordinates[i], y_coordinates[j]] == [2, 1]:
            x1 = x[i]
            y1 = y[j]
            addr1 = i
            addr2 = j
            #print( x1, addr1,':', y1, addr2)

            #print('yes1')

            index =[(a, swap_add.index(x1))for a, swap_add in enumerate(swap_1_2_summary) if x1 in swap_add]
            index2 = [(a, swap_add.index(y1))for a, swap_add in enumerate(swap_1_2_summary) if y1 in swap_add]
            for v in range(0,len(index)-1):
                pos1 = index[v][0]
                vio1 = swap_1_2_summary[pos1][2]
                for v2 in range(0,len(index2)-1):
                    pos2 = index2[v2][0]
                    vio2 = swap_1_2_summary[pos2][2]
                    if pos1 == pos2:
                        vio = vio1
                        #y1 = vio
                        if vio == 1:
                            x1_coordinates.append(x1)
                            y1_coordinates.append(y1)
                    else:
                        vio = 0

        elif [x_coordinates[i], y_coordinates[j]] == [0, -1]:
            x1 = x[i]
            y1 = y[j]
            addr1 = i
            addr2 = j
            #print( x1, addr1,':', y1, addr2)

            #print('yes1')

            index =[(a, swap_add.index(x1))for a, swap_add in enumerate(swap_1_2_summary) if x1 in swap_add]
            index2 = [(a, swap_add.index(y1))for a, swap_add in enumerate(swap_1_2_summary) if y1 in swap_add]
            for v in range(0,len(index)-1):
                pos1 = index[v][0]
                vio1 = swap_1_2_summary[pos1][2]
                for v2 in range(0,len(index2)-1):
                    pos2 = index2[v2][0]
                    vio2 = swap_1_2_summary[pos2][2]
                    if pos1 == pos2:
                        vio = vio1
                        #y1 = vio
                        if vio == 1:
                            x1_coordinates.append(x1)
                            y1_coordinates.append(y1)
                    else:
                        vio = 0
        elif [x_coordinates[i], y_coordinates[j]] == [-1, 0]:
            x1 = x[i]
            y1 = y[j]
            addr1 = i
            addr2 = j
            #print( x1, addr1,':', y1, addr2)

            #print('yes1')

            index =[(a, swap_add.index(x1))for a, swap_add in enumerate(swap_1_2_summary) if x1 in swap_add]
            index2 = [(a, swap_add.index(y1))for a, swap_add in enumerate(swap_1_2_summary) if y1 in swap_add]
            for v in range(0,len(index)-1):
                pos1 = index[v][0]
                vio1 = swap_1_2_summary[pos1][2]
                for v2 in range(0,len(index2)-1):
                    pos2 = index2[v2][0]
                    vio2 = swap_1_2_summary[pos2][2]
                    if pos1 == pos2:
                        vio = vio1
                        #y1 = vio
                        if vio == 1:
                            x1_coordinates.append(x1)
                            y1_coordinates.append(y1)
                    else:
                        vio = 0

        elif [x_coordinates[i], y_coordinates[j]] == [1, -1]:
            x1 = x[i]
            y1 = y[j]
            addr1 = i
            addr2 = j
            #print( x1, addr1,':', y1, addr2)

            #print('yes1')

            index =[(a, swap_add.index(x1))for a, swap_add in enumerate(swap_1_2_summary) if x1 in swap_add]
            index2 = [(a, swap_add.index(y1))for a, swap_add in enumerate(swap_1_2_summary) if y1 in swap_add]
            for v in range(0,len(index)-1):
                pos1 = index[v][0]
                vio1 = swap_1_2_summary[pos1][2]
                for v2 in range(0,len(index2)-1):
                    pos2 = index2[v2][0]
                    vio2 = swap_1_2_summary[pos2][2]
                    if pos1 == pos2:
                        vio = vio1
                        #y1 = vio
                        if vio == 1:
                            x1_coordinates.append(x1)
                            y1_coordinates.append(y1)
                    else:
                        vio = 0
        elif [x_coordinates[i], y_coordinates[j]] == [-1, 1]:
            x1 = x[i]
            y1 = y[j]
            addr1 = i
            addr2 = j
            #print( x1, addr1,':', y1, addr2)

            #print('yes1')

            index =[(a, swap_add.index(x1))for a, swap_add in enumerate(swap_1_2_summary) if x1 in swap_add]
            index2 = [(a, swap_add.index(y1))for a, swap_add in enumerate(swap_1_2_summary) if y1 in swap_add]
            for v in range(0,len(index)-1):
                pos1 = index[v][0]
                vio1 = swap_1_2_summary[pos1][2]
                for v2 in range(0,len(index2)-1):
                    pos2 = index2[v2][0]
                    vio2 = swap_1_2_summary[pos2][2]
                    if pos1 == pos2:
                        vio = vio1
                        #y1 = vio
                        if vio == 1:
                            x1_coordinates.append(x1)
                            y1_coordinates.append(y1)
                    else:
                        vio = 0

        elif [x_coordinates[i], y_coordinates[j]] == [2, -1]:
            x1 = x[i]
            y1 = y[j]
            addr1 = i
            addr2 = j
            #print( x1, addr1,':', y1, addr2)

            #print('yes1')

            index =[(a, swap_add.index(x1))for a, swap_add in enumerate(swap_1_2_summary) if x1 in swap_add]
            index2 = [(a, swap_add.index(y1))for a, swap_add in enumerate(swap_1_2_summary) if y1 in swap_add]
            for v in range(0,len(index)-1):
                pos1 = index[v][0]
                vio1 = swap_1_2_summary[pos1][2]
                for v2 in range(0,len(index2)-1):
                    pos2 = index2[v2][0]
                    vio2 = swap_1_2_summary[pos2][2]
                    if pos1 == pos2:
                        vio = vio1
                        #y1 = vio
                        if vio == 1:
                            x1_coordinates.append(x1)
                            y1_coordinates.append(y1)
                    else:
                        vio = 0
        elif [x_coordinates[i], y_coordinates[j]] == [-1, 2]:
            x1 = x[i]
            y1 = y[j]
            addr1 = i
            addr2 = j
            #print( x1, addr1,':', y1, addr2)

            #print('yes1')

            index =[(a, swap_add.index(x1))for a, swap_add in enumerate(swap_1_2_summary) if x1 in swap_add]
            index2 = [(a, swap_add.index(y1))for a, swap_add in enumerate(swap_1_2_summary) if y1 in swap_add]
            for v in range(0,len(index)-1):
                pos1 = index[v][0]
                vio1 = swap_1_2_summary[pos1][2]
                for v2 in range(0,len(index2)-1):
                    pos2 = index2[v2][0]
                    vio2 = swap_1_2_summary[pos2][2]
                    if pos1 == pos2:
                        vio = vio1
                        #y1 = vio
                        if vio == 1:
                            x1_coordinates.append(x1)
                            y1_coordinates.append(y1)
                    else:
                        vio = 0
        else:
            x1 = x_coordinates[i]
            y1 = y_coordinates[j]
            vio = 0
            #y1 = vio
        x1_coordinates.append(x1)
        y1_coordinates.append(y1)
        vio_list.append(vio)
        #print(i,j)

#print(x1_coordinates)
#print(y1_coordinates)
#print(len(swap_1_2_summary))

f = plt.figure()
f.set_figwidth(20)
f.set_figheight(30)

binvalues, _, _, _ = plt.hist2d(x1_coordinates, y1_coordinates, bins=[x, y], cmap=cmap)
#binvalues2, _, _, _ = plt.hist2d(x1_coordinates, y1_coordinates, bins=[x, y], cmap=cmap, cmin=0.5, vmin=0, vmax=pivot_value)
#
#
binvalues = binvalues.astype(int)
#print(binvalues)

for i in range(len(x) - 1):
    for j in range(len(y) - 1):

        plt.text((x[i] + x[i + 1]) / 2, (y[j] + y[j + 1]) / 2,[x_coordinates[i],y_coordinates[j]],
                 color='white' if binvalues[i, j] < pivot_value else 'black',
                 ha='center', va='center', size=8)


plt.yticks(y)
plt.xticks(x, rotation=90)
plt.gca().invert_yaxis()
plt.grid(True, ls='-', lw=1, color='black')

plt.show()
