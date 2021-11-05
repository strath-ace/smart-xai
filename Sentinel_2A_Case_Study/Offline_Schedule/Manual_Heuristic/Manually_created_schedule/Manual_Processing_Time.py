import datetime as dt
import itertools

import numpy as np

from Sentinel_2A_Case_Study.Environment.Land_visibility import country_access
from Sentinel_2A_Case_Study.Environment.Shade_exposure import eclipse
from Sentinel_2A_Case_Study.Environment.ground_station_access import xband_stations


def processing_time(day, month, year, country):
    path = '../../../Environment/'
    time_interval = 5
    time_second_interval = dt.datetime.strptime('00:00:01.52', '%H:%M:%S.%f') - dt.datetime(1900, 1, 1)
    country_access_summary = country_access(path, time_interval, day, month, year, country)[1]
    stations_summary = xband_stations(path, time_interval, day, month, year)[1]
    eclipse_final = eclipse(path, time_interval, day, month, year)[1]

    idle_time = []
    Total_Table = [[country_access_summary, stations_summary, eclipse_final]]
    Total_Table = list(itertools.chain.from_iterable(list(itertools.chain.from_iterable(Total_Table))))
    sort_list = sorted(Total_Table, key=lambda x: x[0])
    np.set_printoptions(threshold=np.inf)
    Total_Table = np.array(sort_list)
    print(Total_Table)
    # print(Total_Table)
    for a in range(0, len(Total_Table)):
        # print(Start_time)
        # print(End_Time)
        for b in range(a, len(Total_Table) - 1):
            if (Total_Table[b][0] >= Total_Table[b - 1][1]) and (Total_Table[b - 1][0] < Total_Table[b - 1][1]):
                # print('first address',Total_Table[b+1][0])
                Satellite_status = 'Process_images'

                idle_start_time = (dt.datetime.strptime(Total_Table[b - 1][1], '%H:%M:%S.%f') - dt.datetime(1900, 1, 1)) + time_second_interval
                idle_end_time = (dt.datetime.strptime(Total_Table[b][0], '%H:%M:%S.%f') - dt.datetime(1900, 1, 1)) - time_second_interval

                idle_duration = idle_end_time - idle_start_time

                if idle_duration >= time_second_interval * 60:
                    # idle_time.append([str(idle_start_time)[:-3],str(idle_end_time)[:-3],str(idle_duration)[:-3], Satellite_status])
                    idle_time.append([str(idle_start_time)[:-3], str(idle_end_time)[:-3], str(idle_duration.total_seconds()), Satellite_status])

        return idle_time,Total_Table,country_access_summary,stations_summary, eclipse_final
