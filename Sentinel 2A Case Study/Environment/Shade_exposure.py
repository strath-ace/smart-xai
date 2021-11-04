
from start_end_points_data import time_select
from collections import namedtuple
import numpy as np
import datetime as dt



#from pympler.tracker import SummaryTracker

satellite_coordinates = namedtuple("satellite_coordinates", ['index', 'day', 'month', 'year', 'time', 'latitude',
                                                             'longitude'])
eclipse_summary = namedtuple("eclipse_summary", ['index', 'day', 'month', 'year', 'start_time', 'stop_time',
                                                 'duration'])
country_vis = namedtuple("country_vis", ['index', 'Country', 'day', 'month', 'year', 'start_time', 'stop_time',
                                         'duration'])
station_access = namedtuple("station_access", ['index', 'day', 'month', 'year', 'start_time', 'stop_time',
                                               'duration'])


##########   Eclipse times
path_Eclipse = '../Environment/Data/SENTINEL-2A_40697_Eclipse_Summary.txt'

f_Eclipse = open(path_Eclipse, "r")

line_count_Eclipse = 0
for line in f_Eclipse:
    if line != "\n":
        line_count_Eclipse += 1
f_Eclipse.close()

f_Eclipse = open(path_Eclipse, "r")
# print(line_count)
node_count_eclipse = line_count_Eclipse
content_eclipse = f_Eclipse.read()
lines_eclipse = content_eclipse.split('\n')

def eclipse(time_interval,day, month, year):
    eclipse_sum = []
    eclipse_final = []
    start_second_interval, end_second_interval = time_select(day,month)
    # for i in range (6,node_count_eclipse+1):
    for i in range(6, node_count_eclipse + 1):
        # print(i)

        line_details_eclipse = lines_eclipse[i].split()
        if line_details_eclipse[10] == 'Moon':
            eclipse_sum.append(eclipse_summary(i - 6, int(line_details_eclipse[0]), str(line_details_eclipse[1]),
                                               int(line_details_eclipse[2]), str(line_details_eclipse[3]),
                                               str(line_details_eclipse[9]), float(line_details_eclipse[11])))
        else:
            eclipse_sum.append(eclipse_summary(i - 6, int(line_details_eclipse[0]), str(line_details_eclipse[1]),
                                               int(line_details_eclipse[2]), str(line_details_eclipse[3]),
                                               str(line_details_eclipse[15]), float(line_details_eclipse[17])))
    for i in range(0, len(eclipse_sum)):
        if eclipse_sum[i].day == day and eclipse_sum[i].month == month and eclipse_sum[i].year == year:
            eclipse_final.append(
                [eclipse_sum[i].start_time, eclipse_sum[i].stop_time, eclipse_sum[i].duration, 'Penumbra Shade'])

    # eclipse_final = list(itertools.chain.from_iterable(list(itertools.chain.from_iterable(eclipse_final))))
    eclipse_final = sorted(eclipse_final, key=lambda x: x[0])
    np.set_printoptions(threshold=np.inf)

    eclipse_final = np.array(eclipse_final)

    day_data_list = []
    # to create a list when day/night occurs out of selected day
    for i in range(0, len(eclipse_final)):
        dn_start = int((dt.datetime.strptime(str(eclipse_final[i][0]), '%H:%M:%S.%f') - dt.datetime(1900, 1,
                                                                                                    1)).total_seconds())
        dn_end = int((dt.datetime.strptime(str(eclipse_final[i][1]), '%H:%M:%S.%f') - dt.datetime(1900, 1,
                                                                                                  1)).total_seconds())

        if i == 0:
            e = start_second_interval
        else:
            e = (day_data_list[len(day_data_list) - 1][1])

        while e >= (start_second_interval) and (e < dn_end):

            if (e < dn_start):
                dn_access = 1
            elif e in range(dn_start, dn_end):
                dn_access = 0
            else:
                dn_access = 1

            day_data_list.append([e, e + time_interval, dn_access])
            e += time_interval

        g = (day_data_list[len(day_data_list) - 1][1])
        while (g >= dn_end) and (g <= end_second_interval) and (i >= len(eclipse_final) - 1):
            dn_access = 1
            day_data_list.append([g, g + time_interval, dn_access])
            g += time_interval

    # print(day_data_list)

    return day_data_list

