# ------------------Copyright (C) 2022 University of Strathclyde and Author ---------------------------------
# --------------------------------- Author: Cheyenne Powell -------------------------------------------------
# ------------------------- e-mail: cheyenne.powell@strath.ac.uk --------------------------------------------

# This function is used for extracting the data of satellites position for a selected day.
# ===========================================================================================================

from Land_visibility import country_access
from ground_station_access import xband_stations
from Shade_exposure import eclipse


def main():

    path = ''
    day = 1
    month = 'Dec'
    year = 2020
    country = 'All'
    time_interval = 5
    # Select the first of the 2 printed data (first is binary data at intervals of 5 seconds, the second is \
    # summary of all times).
    country_data_list = country_access(path, time_interval, day, month, year, country)[0]
    gnd_data_list = xband_stations(path, time_interval, day, month, year)[0]
    day_data_list = eclipse(path, time_interval, day, month, year)[0]

    print(len(country_data_list))
    print(len(gnd_data_list))
    print(len(day_data_list))
main()