import random
from ortools.sat import sat_parameters_pb2
from ortools.sat.python import cp_model
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from ortools.constraint_solver import routing_enums_pb2,pywrapcp
from ortools.linear_solver import pywraplp
import pandas as pd
import datetime as dt
from matplotlib.dates import DateFormatter, date2num

path = 'C:/Users/User/Documents/PhD/ESA/Satellite data/Sentinel 2/Sentinel2A/timelines_adjusted_millisec_all_countries.txt'


f_coord = open(path, "r")
line_count_coord = 0
for line in f_coord:
    if line != "\n":
        line_count_coord += 1
f_coord.close()

f_coord = open(path, "r")
# print(line_count)
node_count_coord = line_count_coord
content_coord = f_coord.read()
lines_coord = content_coord.split('\n')

#print(node_count_coord)


#model2 = cp_model.CpModel()

# Actives = [model2.NewBoolVar('Actives_%i' % v) for v in range(0, len(final_jobs))]
onboard_mem = 24 * 10 ** 11
# memory required per image
image_mem = 2688 * 10 ** 6
downlink_data_rate = -280 * 10 ** 6
# 5Kbit/s to process images
process_im_mem = 5 * 10 ** 3

Demands_mem = []
start_ints = []
Actives = []
tasks_list = []
weights2 = []
final_total=[]
Actives_List =[]
h_list=[]
end=[]
duration=[]
time_interval = 1

for task in range(0, node_count_coord):
#for task in range(0,2):
    line_details = lines_coord[task].split()
    final_end = int(line_details[2])
    final_start = int(line_details[1])
    final_jobs = line_details[4]
    final_duration = int(line_details[3])

    h = 0


    while h <= (int(final_end / 1000) - int(final_start / 1000)):
        # for i in range(int(final_start[task]/1000),int(final_end[task]/1000)):
        start = int(final_start / 1000) + h
        tasks = final_jobs

        if final_jobs == '1':
            weight2 = 3
            pic_chosen = random.randint(0, 1)
            Demands = image_mem * 1 *time_interval
        elif final_jobs == '2':
            weight2 = 2
            Demands = process_im_mem * time_interval
        elif final_jobs == '3':
            weight2 = 0
            Demands = 0
        elif final_jobs == '4':
            weight2 = 1
            Demands = (downlink_data_rate) * time_interval
        else:
            weight2 = 0
            Demands = 0

        total = Demands

        if h == 0 and len(final_total) ==0 and total>=0:
            total = Demands
            Actives = True

        elif h == 0 and len(final_total) ==0 and total<0:
            total = 0
            Actives = False

        elif h== 0 and final_total[h - 1] > 0 and Demands != 0:
            total = final_total[h - 1] + Demands

            if total > 0 and total <= onboard_mem:
                total = Demands + final_total[h - 1]
                Actives = True
            else:
                total = final_total[h - 1]
                Actives = False

        elif  h>0 and final_total[len(final_total)-1] > 0 and Demands !=0 :
            total = final_total[len(final_total)-1]  + Demands

            if total > 0 and total <= onboard_mem:
                total = Demands + final_total[len(final_total)-1]
                Actives = True
            else:
                total = final_total[len(final_total)-1]
                Actives = False

        elif (h==0 or h>0) and final_total[len(final_total)-1] == 0 and Demands !=0 :
            total = final_total[len(final_total)-1]  + Demands

            if total > 0 and total <= onboard_mem:
                total = Demands + final_total[len(final_total)-1]
                Actives = True
            else:
                total = final_total[len(final_total)-1]
                Actives = False

        elif Demands ==0:
            total = Demands + final_total[len(final_total)-1]
            Actives =False

        final_total.append(total)


            # print(i)
        #final_total.append(total)
        Demands_mem.append(Demands)
        start_ints.append(start)
        end.append(start+time_interval)
        duration.append(time_interval)
        tasks_list.append(tasks)
        weights2.append(weight2)
        Actives_List.append(Actives)
        h_list.append(h)
        h += time_interval

print_list=[]
print_list2=[]
for i in range (0, len(tasks_list)):


    print([str(dt.timedelta(seconds=(start_ints[i]))), tasks_list[i], Demands_mem[i], h_list[i],final_total[i]],Actives_List[i])

    print_list.append([str(dt.timedelta(seconds=(start_ints[i]))),str(dt.timedelta(seconds=(end[i]))), tasks_list[i], Demands_mem[i], h_list[i],final_total[i], Actives_List[i]])
    print_list2.append([start_ints[i],end[i], tasks_list[i], Demands_mem[i], h_list[i],final_total[i], Actives_List[i]])

file1 = open("memory_states_seconds.txt", "w")
df1 = pd.DataFrame(print_list2)
file1.writelines(df1.to_string(header=False, index=False))
file1.close()

file2 = open("memory_states.txt", "w")
df2 = pd.DataFrame(print_list)
file2.writelines(df2.to_string(header=False, index=False))
#
#file2.writelines(str(print_list))
file2.close()



x=pd.DataFrame({'Time':[str(dt.timedelta(seconds=(start_ints[i]))) for i in range (0, len(tasks_list))]})
#x['Time'] = pd.to_timedelta(x['Time'])

#x=start_ints
y=final_total
#plt.plot(x, y,label='line1')
#plt.plot(x, y1,label='line2')
#plt.bar(x,y,width = 0.8, color = 'green')
#plt.title('Memory chart!')
# plt.xlabel('x - axis')
# plt.ylabel('y - axis')
#plt.plot([],[])
#plt.scatter(x,y)
x['Time'] = pd.to_datetime(x['Time'])
fig, ax = plt.subplots()

myFmt = DateFormatter("%H:%M:%S")
ax.xaxis.set_major_formatter(myFmt)

ax.plot(x['Time'],y)

plt.gcf().autofmt_xdate()

#plt.gca()

#myFmt = mdates.DateFormatter('%H:%M')
#plt.gca().xaxis.set_major_formatter(myFmt)
# plt.legend()
plt.show()