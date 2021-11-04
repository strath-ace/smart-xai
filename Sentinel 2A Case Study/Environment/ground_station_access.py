from start_end_points_data import time_select
from collections import namedtuple
import numpy as np
import datetime as dt


station_access = namedtuple("station_access", ['index', 'day', 'month', 'year', 'start_time', 'stop_time',
                                               'duration'])

# Xband to ground stations
path_station = '../Environment/Data/Facility-EUMETSAT_Maspalomas-To-Satellite-Satellite-Sensor-XBand_Access.txt'
f_station = open(path_station, "r")
content_station = f_station.read()
lines_station = content_station.split('\n')


def Xband_stations(time_interval,day, month, year):
    station_accesses = []
    station_accesses1 = []
    station_accesses2 = []
    station_accesses3 = []
    stations_summary = []

    start_second_interval, end_second_interval = time_select(day,month)
    Xband = 'Eumetsat'

    # for a in range (0,4):
    for a in range(0, 4):
        # while Xband != '':
        # print(a)
        if Xband == 'Eumetsat':

            for i in range(8, 864):
                # for i in range(8, 10 + 1):
                # print(i)
                line_details_station = lines_station[i].split()
                station_accesses.append(
                    station_access(i - 8, int(line_details_station[1]), str(line_details_station[2]),
                                   int(line_details_station[3]), str(line_details_station[4]),
                                   str(line_details_station[8]), float(line_details_station[9])))
            # print(station_accesses)
            for i in range(0, len(station_accesses)):
                if station_accesses[i].day == day and station_accesses[i].month == month and station_accesses[
                    i].year == year:
                    stations_summary.append([station_accesses[i].start_time, station_accesses[i].stop_time,
                                             station_accesses[i].duration, Xband])

            Xband = 'Matera'

            # return stations_summary

        elif Xband == 'Matera':
            i = 874
            for i in range(876, 1917):
                # for i in range(876, 879 + 1):
                # print(i)
                line_details_station = lines_station[i].split()
                station_accesses1.append(
                    station_access(i - 876, int(line_details_station[1]), str(line_details_station[2]),
                                   int(line_details_station[3]), str(line_details_station[4]),
                                   str(line_details_station[8]), float(line_details_station[9])))
                # print(station_accesses)
            for i in range(0, len(station_accesses1)):
                if station_accesses1[i].day == day and station_accesses1[i].month == month and station_accesses1[
                    i].year == year:
                    stations_summary.append(
                        [station_accesses1[i].start_time, station_accesses1[i].stop_time,
                         station_accesses1[
                             i].duration, Xband])
            Xband = 'PrudhoeBay'

            # return stations_summary

        elif Xband == 'PrudhoeBay':
            i = 1928
            for i in range(1929, 4096):
                # for i in range(1929, 1930 + 1):
                # print(i)
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
                            i].duration, Xband])
            Xband = 'Svalbard'

            # return stations_summary

        elif Xband == 'Svalbard':
            i = 4107
            for i in range(4108, 6510):
                # for i in range(4108, 4110 + 1):
                # print(i)
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
                            i].duration, Xband])

            Xband = ''

        else:

            print('Error no data found')

    stations_summary = sorted(stations_summary, key=lambda x: x[0])
    np.set_printoptions(threshold=np.inf)

    stations_summary = np.array(stations_summary)

    gnd_data_list = []

    # to create a list where ground station is visible out of selected day
    for i in range(0, len(stations_summary)):
        ground_start = int((dt.datetime.strptime(str(stations_summary[i][0]), '%H:%M:%S.%f') - dt.datetime(1900,
                                                                                                           1,
                                                                                                           1)).total_seconds())
        ground_end = int((dt.datetime.strptime(str(stations_summary[i][1]), '%H:%M:%S.%f') - dt.datetime(1900, 1,
                                                                                                         1)).total_seconds())

        if i == 0:
            e = start_second_interval
        else:
            e = (gnd_data_list[len(gnd_data_list) - 1][1])

        while e >= (start_second_interval) and (e < ground_end):

            if (e < ground_start):
                gnd_access = 0
            elif e in range(ground_start, ground_end):
                gnd_access = 1
            else:
                gnd_access = 0

            gnd_data_list.append([e, e + time_interval, gnd_access])
            e += time_interval

        g = (gnd_data_list[len(gnd_data_list) - 1][1])
        while (g >= ground_end) and (g <= end_second_interval) and (i >= len(stations_summary) - 1):
            gnd_access = 0
            gnd_data_list.append([g, g + time_interval, gnd_access])
            g += time_interval
    return gnd_data_list




