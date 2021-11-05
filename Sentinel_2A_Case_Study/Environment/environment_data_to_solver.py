import sys
from Sentinel_2A_Case_Study.Environment.Land_visibility import country_access
from Sentinel_2A_Case_Study.Environment.ground_station_access import xband_stations
from Sentinel_2A_Case_Study.Environment.Shade_exposure import eclipse


def environment_data(path,time_interval, day, month, year, country):
    # tracker = SummaryTracker()




    # select the first of the 2 printed data (first is binary data at intervals of 5 seconds, the second is summary of all times)
    country_data_list = country_access(path,time_interval, day, month, year, country)[0]
    gnd_data_list = xband_stations(path,time_interval, day, month, year)[0]
    day_data_list = eclipse(path,time_interval, day, month, year)[0]

    print(len(country_data_list))
    print(len(gnd_data_list))
    print(len(day_data_list))

    return country_data_list, gnd_data_list, day_data_list
