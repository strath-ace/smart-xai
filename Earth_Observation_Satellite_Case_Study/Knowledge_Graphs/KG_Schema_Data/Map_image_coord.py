# ------------------Copyright (C) 2022 University of Strathclyde and Author ---------------------------------
# --------------------------------- Author: Cheyenne Powell -------------------------------------------------
# ------------------------- e-mail: cheyenne.powell@strath.ac.uk --------------------------------------------

# Program used to extract all the satellite coordinates
# ===========================================================================================================




import datetime as dt
from collections import namedtuple

satellite_coordinates = namedtuple("satellite_coordinates", ['index', 'day', 'month', 'year', 'time', 'latitude',
                                                             'longitude'])

def sat_coordinates(day, month, year, path):
    # Coordinate txt file imported.
    # path_coord = '/Earth_Observation_Satellite_Case_Study/Environment/Data/Satellite_Coordinates/Position1.txt'
    # print('path', os.getcwd())
    path_coord = path + 'Data/Satellite_Coordinates/Position1.txt'

    sat_coord = open(path_coord, "r")
    memory_count_coord = 0
    for line in sat_coord:
        if line != "\n":
            memory_count_coord += 1
    sat_coord.close()

    sat_coord = open(path_coord, "r")
    # print(line_count)
    memory_count_coord = memory_count_coord
    sat_coord = sat_coord.read()
    sat_coord = sat_coord.split('\n')

    satellite_coord_summary_time = []
    satellite_coord = []
    satellite_coord_summary = []

    start = 46810
    increment = 86402
    increment1 = 86405
    day_start = start + (increment * (day - 2))
    day_end = start + (increment1 * (day - 1))

    for i in range(day_start, day_end+1):
        #print(i)
        coord = sat_coord[i].split()
        satellite_coord.append(satellite_coordinates(i - day_start, int(coord[0]), str(coord[1]), int(coord[2]),
                                                     str(coord[3]), float(coord[4]), float(coord[5])))

    #print(satellite_coord)
    for i in range(0, len(satellite_coord)):
        # print(satellite_coord[i].latitude,satellite_coord[i].longitude)
        if satellite_coord[i].day == day and satellite_coord[i].month == month and satellite_coord[i].year == year:

            satellite_coord_summary.append([int((dt.datetime.strptime(str(satellite_coord[i].time), '%H:%M:%S.%f') - dt.datetime(1900, 1, 1)).total_seconds()), satellite_coord[i].latitude, satellite_coord[i].longitude, 'Satellite Coordinates'])
            satellite_coord_summary_time.append([satellite_coord[i].time, satellite_coord[i].latitude, satellite_coord[i].longitude, 'Satellite Coordinates'])


    return satellite_coord_summary

def main():
    print('test')
    day = 3
    month = 'Dec'
    year = 2020
    print(sat_coordinates(day, month, year, '../../Environment/'))

main()
