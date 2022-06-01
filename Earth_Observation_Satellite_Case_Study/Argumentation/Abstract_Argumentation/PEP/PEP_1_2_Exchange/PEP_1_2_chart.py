import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import datetime as dt
import plotly.figure_factory as ff
import plotly
from matplotlib.dates import DateFormatter
import plotly.express as px
import numpy as np
from matplotlib import colors
from matplotlib.colors import ListedColormap
from Earth_Observation_Satellite_Case_Study.Environment.environment_data_to_solver import environment_data


day = 3



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

datastart = 15000
#dataend = count_attack_coord-2270
dataend = count_attack_coord-2100
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

# create a colormap with two colors, vmin and vmax are chosen so that their center is the pivot value
cmap = ListedColormap(['indigo', 'gold'])


pivot_value = 1
#x_coordinates=[1,0,2,2,1,0,3,1]
x_coordinates=np.array(x_coordinates)
#y_coordinates=[1,0,2,2,1,0,3,1]

print(x)
y_coordinates=np.array(y_coordinates)
# print(x_coordinates)
# print(y_coordinates)

x1_coordinates=[]
y1_coordinates=[]
for i in range(len(x) - 1):
    for j in range(len(y) - 1):

        if  [x_coordinates[i], y_coordinates[j]] == [0, 1]:
            x1 = x[i]
            y1 = y[j]
            pic_addr = i
            proc_addr = j
            print( x1, pic_addr,':',y1,proc_addr)
            #mem_violation = PEP_1_2_Swap(datastart, dataend,i,j)

        elif [x_coordinates[i], y_coordinates[j]] == [1, 0]:
            x1 = x[i]
            y1 = y[j]
            proc_addr = i
            pic_addr = j
            print( y1, pic_addr,':',x1,proc_addr)
        else:
            x1 = x_coordinates[i]
            y1 = y_coordinates[j]
        x1_coordinates.append(x1)
        y1_coordinates.append(y1)
        #print(i,j)

# print(x1_coordinates)
# print(y1_coordinates)

f = plt.figure()
f.set_figwidth(40)
f.set_figheight(40)
binvalues, _, _, _ = plt.hist2d(x1_coordinates, y1_coordinates, bins=[x, y], cmap=cmap, vmin=0, vmax=pivot_value)


binvalues = binvalues.astype(int)
print(binvalues)

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
# x_coordinates = np.random.uniform(x1.min(), x1.max(), size=40000)
# y_coordinates = np.random.uniform(y1.min(), y1.max(), size=40000)



#
# # data = np.random.rand(max_number+1, max_number+1) * 20
# # #print(data)
# # # create discrete colormap
# # cmap = colors.ListedColormap(['red','green'])
# #
# # bounds = [0, max_number+1, 20]
# # norm = colors.BoundaryNorm(bounds, cmap.N)
# fig, ax = plt.subplots()
# #ax.imshow(data, cmap=cmap, norm=norm)
#
# #draw grids
# ax.grid(which='major', axis='both', linestyle='-', color='k')
# ax.set_xticks(np.arange(min_number, max_number+1, 5))
# ax.set_yticks(np.arange(min_number, max_number+1, 5))
#
# ax.set_ylim(ymin=min_number)
# ax.set_ylim(ymax=max_number+1)
# ax.set_xlim(xmin=min_number)
# ax.invert_yaxis()
#
# plt.show()

