# This function generates the processing times based on the gaps between the actions within a given day

import datetime as dt
import itertools
import numpy as np

from Sentinel_2A_Case_Study.Environment.Land_visibility import country_access
from Sentinel_2A_Case_Study.Environment.Shade_exposure import eclipse
from Sentinel_2A_Case_Study.Environment.ground_station_access import xband_stations


# function used to manually add time for processing in the list of actions based on the availability between each estimated action
def processing_time(day, month, year, country, time_interval):
    path = '../../../Environment/'

    time_second_interval = dt.datetime.strptime('00:00:01.52', '%H:%M:%S.%f') - dt.datetime(1900, 1, 1)
    country_access_summary = country_access(path, time_interval, day, month, year, country)[1]
    stations_summary = xband_stations(path, time_interval, day, month, year)[1]
    eclipse_final = eclipse(path, time_interval, day, month, year)[1]

    idle_time = []
    # create table based on imported lists from the satellites position (country visual, ground station access, light/shade exposure
    Total_Table = [[country_access_summary, stations_summary, eclipse_final]]
    Total_Table = list(itertools.chain.from_iterable(list(itertools.chain.from_iterable(Total_Table))))
    sort_list = sorted(Total_Table, key=lambda x: x[0])
    np.set_printoptions(threshold=np.inf)
    Total_Table = np.array(sort_list)
    # print(Total_Table)

    for a in range(0, len(Total_Table)):

        for b in range(a, len(Total_Table) - 1):
            if (Total_Table[b][0] >= Total_Table[b - 1][1]) and (Total_Table[b - 1][0] < Total_Table[b - 1][1]):

                Satellite_status = 'Process_images'
                idle_start_time = (dt.datetime.strptime(Total_Table[b - 1][1], '%H:%M:%S.%f') - dt.datetime(1900, 1, 1)) + time_second_interval
                idle_end_time = (dt.datetime.strptime(Total_Table[b][0], '%H:%M:%S.%f') - dt.datetime(1900, 1, 1)) - time_second_interval

                idle_duration = idle_end_time - idle_start_time
                # if idle time is greater than 1 minute
                if idle_duration >= time_second_interval * 60:
                    idle_time.append([str(idle_start_time)[:-3], str(idle_end_time)[:-3], str(idle_duration.total_seconds()), Satellite_status])
        # idle time in the form -  start, end, duration and status - Process
        # total table in the form - start, end, duration and status - Land, light/shade exposure, ground station access
        # country access in the form - start, end, duration and status - Land
        # stations summary in the form of - start, end, duration and status - ground station access
        # eclipse final in the form of - start, end, duration and status - light/shade exposure
        return idle_time, Total_Table, country_access_summary, stations_summary, eclipse_final
