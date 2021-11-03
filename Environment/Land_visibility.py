from start_end_points_data import time_select
from collections import namedtuple
import numpy as np
import datetime as dt


country_vis = namedtuple("country_vis", ['index', 'Country', 'day', 'month', 'year', 'start_time', 'stop_time',
                                         'duration'])


# Visual of countries
path_country = '../Land Coverage/all countries2.txt'
f_country = open(path_country, "r")

line_count_country = 0
for line in f_country:
    if line != "\n":
        line_count_country += 1
f_country.close()

f_country = open(path_country, "r")
# print(line_count)
node_count_country = line_count_country
content_country = f_country.read()
lines_country = content_country.split('\n')



def country_access(time_interval,day, month, year, country):
    country_accesses = []
    country_access_summary = []

    start_second_interval, end_second_interval = time_select(day,month)

    for i in range(6, node_count_country + 1):
        # for i in range(6, 8 + 1):
        # print(i)
        line_details_country = lines_country[i].split()
        country_accesses.append(country_vis(i - 6, str(line_details_country[0]), int(line_details_country[1]),
                                            str(line_details_country[2]), int(line_details_country[3]),
                                            str(line_details_country[4]), str(line_details_country[8]),
                                            float(line_details_country[9])))


    for i in range(0, len(country_accesses)):
        if country == 'All' or country == '':
            if country_accesses[i].day == day and country_accesses[i].month == month and country_accesses[
                i].year == year:
                country_access_summary.append(
                    [country_accesses[i].start_time, country_accesses[i].stop_time, country_accesses[i].duration,
                     'Land'])
        else:
            if country_accesses[i].day == day and country_accesses[i].month == month and country_accesses[
                i].year == year and country_accesses[i].Country == country:
                country_access_summary.append(
                    [country_accesses[i].start_time, country_accesses[i].stop_time, country_accesses[i].duration,
                     'Land'])

    country_access_summary = sorted(country_access_summary, key=lambda x: x[0])
    np.set_printoptions(threshold=np.inf)

    country_access_summary = np.array(country_access_summary)
    #print(len(country_access_summary))
    country_data_list = []
    # to create a list where land is visible out of slected day
    for i in range(0, len(country_access_summary)):
        country_start = int((dt.datetime.strptime(str(country_access_summary[i][0]), '%H:%M:%S.%f') - dt.datetime(1900, 1,
                                                                                                                  1)).total_seconds())
        country_end = int((dt.datetime.strptime(str(country_access_summary[i][1]), '%H:%M:%S.%f') - dt.datetime(1900, 1,
                                                                                                                1)).total_seconds())
        #print(i)
        if i == 0:
            e = start_second_interval
        else:
            e = (country_data_list[len(country_data_list) - 1][1])
        #print(e,country_start, country_end)
        while (e >= start_second_interval) and (e < country_end):
            #print('True')
            if e < country_start:
                c_access = 0
            elif e in range(country_start, country_end):
                c_access = 1
            else:
                c_access = 0

            country_data_list.append([e, e + time_interval, c_access])
            #print((country_data_list))
            e += time_interval

        g = (country_data_list[len(country_data_list) - 1][1])
        while (g >= country_end) and (g <= end_second_interval) and (i >= len(country_access_summary) - 1):
            c_access = 0
            country_data_list.append([g, g + time_interval, c_access])
            g += time_interval
    return country_data_list





