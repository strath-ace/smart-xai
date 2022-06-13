# ------------------Copyright (C) 2022 University of Strathclyde and Author ---------------------------------
# --------------------------------- Author: Cheyenne Powell -------------------------------------------------
# ------------------------- e-mail: cheyenne.powell@strath.ac.uk --------------------------------------------

# This file is used for generating data where light/shade exposures occur over a selected day.
# ===========================================================================================================

from collections import namedtuple
import numpy as np
import datetime as dt
from Earth_Observation_Satellite_Case_Study.Environment.start_end_points_data import time_select

satellite_coordinates = namedtuple("satellite_coordinates", ['index', 'day', 'month', 'year', 'time', 'latitude',
                                                             'longitude'])
eclipse_summary = namedtuple("eclipse_summary", ['index', 'day', 'month', 'year', 'start_time', 'stop_time',
                                                 'duration'])
country_vis = namedtuple("country_vis", ['index', 'Country', 'day', 'month', 'year', 'start_time', 'stop_time',
                                         'duration'])
station_access = namedtuple("station_access", ['index', 'day', 'month', 'year', 'start_time', 'stop_time',
                                               'duration'])


def eclipse(path, time_interval, day, month, year):

    # Light/shade exposure txt file imported.
    path_eclipse = path + 'Data/Light_Shade_exposure.txt'
    f_eclipse = open(path_eclipse, "r")
    line_count_eclipse = 0
    for line in f_eclipse:
        if line != "\n":
            line_count_eclipse += 1
    f_eclipse.close()

    f_eclipse = open(path_eclipse, "r")
    node_count_eclipse = line_count_eclipse
    content_eclipse = f_eclipse.read()
    lines_eclipse = content_eclipse.split('\n')

    eclipse_sum = []
    eclipse_final = []
    # Import function to determine start and end time of the day.
    start_second_interval, end_second_interval = time_select(day, month)

    # Extraction of all shade instances from the list.
    for i in range(6, node_count_eclipse + 1):

        line_details_eclipse = lines_eclipse[i].split()
        if line_details_eclipse[10] == 'Moon':
            eclipse_sum.append(eclipse_summary(i - 6, int(line_details_eclipse[0]), str(line_details_eclipse[1]),
                                               int(line_details_eclipse[2]), str(line_details_eclipse[3]),
                                               str(line_details_eclipse[9]), float(line_details_eclipse[11])))
        else:
            eclipse_sum.append(eclipse_summary(i - 6, int(line_details_eclipse[0]), str(line_details_eclipse[1]),
                                               int(line_details_eclipse[2]), str(line_details_eclipse[3]),
                                               str(line_details_eclipse[15]), float(line_details_eclipse[17])))

    # Extraction of data containing shade exposure based on the date selected.
    for i in range(0, len(eclipse_sum)):
        if eclipse_sum[i].day == day and eclipse_sum[i].month == month and eclipse_sum[i].year == year:
            eclipse_final.append(
                [eclipse_sum[i].start_time, eclipse_sum[i].stop_time, eclipse_sum[i].duration, 'Penumbra Shade'])

    # Sort list in ascending order based on start time - list contains the full summary based on the date selected.
    eclipse_final = sorted(eclipse_final, key=lambda x: x[0])
    np.set_printoptions(threshold=np.inf)
    eclipse_final = np.array(eclipse_final)

    day_data_list = []

    # To create a boolean list when day/night occurs out of selected day using the start and end time for the\
    # day and each action.
    for i in range(0, len(eclipse_final)):
        dn_start = int((dt.datetime.strptime(str(eclipse_final[i][0]), '%H:%M:%S.%f') - dt.datetime(1900, 1,
                                                                                                    1)).total_seconds())
        dn_end = int((dt.datetime.strptime(str(eclipse_final[i][1]), '%H:%M:%S.%f') - dt.datetime(1900, 1,
                                                                                                  1)).total_seconds())
        if i == 0:
            e = start_second_interval
        else:
            e = (day_data_list[len(day_data_list) - 1][1])

        while e >= start_second_interval and (e < dn_end):

            if e < dn_start:
                dn_access = 1
            elif e in range(dn_start, dn_end):
                dn_access = 0
            else:
                dn_access = 1

            day_data_list.append([e, e + time_interval, dn_access])
            e += time_interval

        g = (day_data_list[len(day_data_list) - 1][1])
        while (g >= dn_end) and (g <= end_second_interval - 5) and (i >= len(eclipse_final) - 1):
            dn_access = 1
            day_data_list.append([g, g + time_interval, dn_access])
            g += time_interval

    # Returns the list of light/shade exposure in boolean form at time intervals of x seconds and returns the\
    # summary of all light/shade times.
    # Day data list, in the form of start, end, and 1/0 based on light exposure - 1 for light, 0 for shade.
    # Eclipse final, contains a summary of shade times in the form of start, end, duration and whether or not\
    # there is an eclipse (shade).
    return day_data_list, eclipse_final
