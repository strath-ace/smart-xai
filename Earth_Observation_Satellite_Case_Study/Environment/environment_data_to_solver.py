# This function is used to send satellites position data to the function solver test

from Earth_Observation_Satellite_Case_Study.Environment.Land_visibility import country_access
from Earth_Observation_Satellite_Case_Study.Environment.ground_station_access import xband_stations
from Earth_Observation_Satellite_Case_Study.Environment.Shade_exposure import eclipse


def environment_data(path, time_interval, day, month, year, country):
    # select the first of the 2 printed data (first is binary data at intervals of 5 seconds, the second is summary of all times)
    country_data_list = country_access(path, time_interval, day, month, year, country)[0]
    gnd_data_list = xband_stations(path, time_interval, day, month, year)[0]
    day_data_list = eclipse(path, time_interval, day, month, year)[0]

    # test to see if the lists are the same length
    print(len(country_data_list))
    print(len(gnd_data_list))
    print(len(day_data_list))

    return country_data_list, gnd_data_list, day_data_list
