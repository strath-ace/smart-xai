# ------------------Copyright (C) 2022 University of Strathclyde and Author ---------------------------------
# --------------------------------- Author: Cheyenne Powell -------------------------------------------------
# ------------------------- e-mail: cheyenne.powell@strath.ac.uk --------------------------------------------

# This function is used to extract all the selected ground station access for an Earth Observation satellite
# for selected day from the txt file
# ===========================================================================================================

import datetime as dt
from collections import namedtuple
import numpy as np
from Earth_Observation_Satellite_Case_Study.Environment.start_end_points_data import time_select

station_access = namedtuple("station_access", ['index', 'day', 'month', 'year', 'start_time', 'stop_time',
                                               'duration'])

def xband_stations(path,time_interval, day, month, year):
    # Xband to ground stations text file imported
    path_station = path+'Data/Ground_stations.txt'
    f_station = open(path_station, "r")
    content_station = f_station.read()
    lines_station = content_station.split('\n')

    station_accesses = []
    station_accesses1 = []
    station_accesses2 = []
    station_accesses3 = []
    stations_summary = []

    # import start and end time of the day function
    start_second_interval, end_second_interval = time_select(day, month)

    #first station initialised is based on the order of the raw text file
    xband = 'Eumetsat'

    # loop for storing the durations the 4 ground stations have communication to the satellite based on the date selected
    for a in range(0, 4):

        if xband == 'Eumetsat':
            # ground station row position number in txt file
            for i in range(8, 864):

                line_details_station = lines_station[i].split()
                station_accesses.append(
                    station_access(i - 8, int(line_details_station[1]), str(line_details_station[2]),
                                   int(line_details_station[3]), str(line_details_station[4]),
                                   str(line_details_station[8]), float(line_details_station[9])))

            for i in range(0, len(station_accesses)):
                if station_accesses[i].day == day and station_accesses[i].month == month and station_accesses[i].year == year:
                    stations_summary.append([station_accesses[i].start_time, station_accesses[i].stop_time, station_accesses[i].duration, xband])

            xband = 'Matera'

        # next ground station in file
        elif xband == 'Matera':
            # ground station row position number in txt file
            for i in range(876, 1917):

                line_details_station = lines_station[i].split()
                station_accesses1.append(
                    station_access(i - 876, int(line_details_station[1]), str(line_details_station[2]),
                                   int(line_details_station[3]), str(line_details_station[4]),
                                   str(line_details_station[8]), float(line_details_station[9])))
                # print(station_accesses)
            for i in range(0, len(station_accesses1)):
                if station_accesses1[i].day == day and station_accesses1[i].month == month and station_accesses1[i].year == year:
                    stations_summary.append([station_accesses1[i].start_time, station_accesses1[i].stop_time, station_accesses1[i].duration, xband])
            xband = 'PrudhoeBay'

        # next ground station in file
        elif xband == 'PrudhoeBay':
            # ground station row position number in txt file
            for i in range(1929, 4096):

                line_details_station = lines_station[i].split()
                station_accesses2.append(
                    station_access(i - 1929, int(line_details_station[1]), str(line_details_station[2]),
                                   int(line_details_station[3]), str(line_details_station[4]),
                                   str(line_details_station[8]), float(line_details_station[9])))
                # print(station_accesses)
            for i in range(0, len(station_accesses2)):
                if station_accesses2[i].day == day and station_accesses2[i].month == month and \
                        station_accesses2[
                            i].year == year:
                    stations_summary.append(
                        [station_accesses2[i].start_time, station_accesses2[i].stop_time, station_accesses2[
                            i].duration, xband])
            xband = 'Svalbard'

        # next ground station in file
        elif xband == 'Svalbard':
            # ground station row position number in txt file
            for i in range(4108, 6510):

                line_details_station = lines_station[i].split()
                station_accesses3.append(
                    station_access(i - 4108, int(line_details_station[1]), str(line_details_station[2]),
                                   int(line_details_station[3]), str(line_details_station[4]),
                                   str(line_details_station[8]), float(line_details_station[9])))
                # print(station_accesses)
            for i in range(0, len(station_accesses3)):
                if station_accesses3[i].day == day and station_accesses3[i].month == month and \
                        station_accesses3[
                            i].year == year:
                    stations_summary.append(
                        [station_accesses3[i].start_time, station_accesses3[i].stop_time, station_accesses3[
                            i].duration, xband])
            # no more stations after all stations have been explored
            xband = ''

        else:

            print('Error no data found')

    # sort list in ascending order based on start time - list contains the full summary based on the date selected
    stations_summary = sorted(stations_summary, key=lambda x: x[0])
    np.set_printoptions(threshold=np.inf)
    stations_summary = np.array(stations_summary)

    gnd_data_list = []

    # to create a boolean list where ground station is visible out of selected day based on start and end time of actions
    for i in range(0, len(stations_summary)):
        ground_start = int((dt.datetime.strptime(str(stations_summary[i][0]), '%H:%M:%S.%f') - dt.datetime(1900,
                                                                                                           1,
                                                                                                           1)).total_seconds())
        ground_end = int((dt.datetime.strptime(str(stations_summary[i][1]), '%H:%M:%S.%f') - dt.datetime(1900, 1,
                                                                                                         1)).total_seconds())

        if i == 0:
            e = start_second_interval
        else:
            e = gnd_data_list[len(gnd_data_list) - 1][1]

        while e >= start_second_interval and (e < ground_end):

            if e < ground_start:
                gnd_access = 0
            elif e in range(ground_start, ground_end):
                gnd_access = 1
            else:
                gnd_access = 0

            gnd_data_list.append([e, e + time_interval, gnd_access])
            e += time_interval

        g = (gnd_data_list[len(gnd_data_list) - 1][1])
        while (g >= ground_end) and (g <= end_second_interval-5) and (i >= len(stations_summary) - 1):
            gnd_access = 0
            gnd_data_list.append([g, g + time_interval, gnd_access])
            g += time_interval

    # returns the list of ground stations in boolean form at time intervals of x seconds and returns the summary of all accessible ground stations
    # ground data list in the form of start, end, and 1/0 based on accessibility of ground stations
    # stations summary is in the form of start, end, duration and whether or not station is accessible
    return gnd_data_list, stations_summary
