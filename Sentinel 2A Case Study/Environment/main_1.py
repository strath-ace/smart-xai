import sys
from Land_visibility import country_access
from ground_station_access import  Xband_stations
from Shade_exposure import eclipse

def main():
    #tracker = SummaryTracker()
    if len(sys.argv) >= 1:
        # day_data_list =[]
        day = 1
        month = 'Dec'
        year = 2020
        country = 'All'
        time_interval = 5

        country_data_list = country_access(time_interval,day, month, year, country)
        gnd_data_list = Xband_stations(time_interval,day, month, year)
        day_data_list = eclipse(time_interval,day, month, year)

        print(len(country_data_list))
        print(len(gnd_data_list))
        print(len(day_data_list))

main()