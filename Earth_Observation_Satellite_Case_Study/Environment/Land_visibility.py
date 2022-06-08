# ------------------Copyright (C) 2022 University of Strathclyde and Author ---------------------------------
# --------------------------------- Author: Cheyenne Powell -------------------------------------------------
# ------------------------- e-mail: cheyenne.powell@strath.ac.uk --------------------------------------------

# This function is used for generating land visibility data for a selected day extracted from the text file.
# ===========================================================================================================

from collections import namedtuple
import numpy as np
import datetime as dt
from Earth_Observation_Satellite_Case_Study.Environment.start_end_points_data import time_select

country_vis = namedtuple("country_vis", ['index', 'Country', 'day', 'month', 'year', 'start_time', 'stop_time',
                                         'duration'])


def country_access(path, time_interval, day, month, year, country):
    # Visual of countries txt file imported.
    path_country = path + 'Data/Land.txt'
    f_country = open(path_country, "r")

    line_count_country = 0
    for line in f_country:
        if line != "\n":
            line_count_country += 1
    f_country.close()

    f_country = open(path_country, "r")

    node_count_country = line_count_country
    content_country = f_country.read()
    lines_country = content_country.split('\n')

    country_accesses = []
    country_access_summary = []

    # import function to determine start and end time of the day.
    start_second_interval, end_second_interval = time_select(day, month)

    # extraction of all lands/countries from the list.
    for i in range(6, node_count_country + 1):
        line_details_country = lines_country[i].split()
        country_accesses.append(country_vis(i - 6, str(line_details_country[0]), int(line_details_country[1]),
                                            str(line_details_country[2]), int(line_details_country[3]),
                                            str(line_details_country[4]), str(line_details_country[8]),
                                            float(line_details_country[9])))
    # If 1 country is of interest, this section will extract the country of interest or if no country is entered,\
    # all countries in list will be used.
    for i in range(0, len(country_accesses)):
        if country == 'All' or country == '':
            if country_accesses[i].day == day and country_accesses[i].month == month and \
                    country_accesses[i].year == year:country_access_summary.append([country_accesses[i].start_time,
                                            country_accesses[i].stop_time, country_accesses[i].duration, 'Land'])
        else:
            if country_accesses[i].day == day and country_accesses[i].month == month and \
                    country_accesses[i].year == year and country_accesses[i].Country == country:
                country_access_summary.append([country_accesses[i].start_time, country_accesses[i].stop_time,
                                               country_accesses[i].duration, 'Land'])
    # To rearrange the list in ascending order of start time.
    # Order is in the form - start, end, duration and land.
    country_access_summary = sorted(country_access_summary, key=lambda x: x[0])
    np.set_printoptions(threshold=np.inf)
    country_access_summary = np.array(country_access_summary)

    country_data_list = []

    # To create a boolean list where land is visible out of the selected day at every time interval t.
    for i in range(0, len(country_access_summary)):
        country_start = int((dt.datetime.strptime(str(country_access_summary[i][0]), '%H:%M:%S.%f')
                             - dt.datetime(1900, 1,1)).total_seconds())
        country_end = int((dt.datetime.strptime(str(country_access_summary[i][1]), '%H:%M:%S.%f')
                           - dt.datetime(1900, 1,1)).total_seconds())
        if i == 0:
            e = start_second_interval
        else:
            e = (country_data_list[len(country_data_list) - 1][1])

        while (e >= start_second_interval) and (e < country_end):

            if e < country_start:
                c_access = 0
            elif e in range(country_start, country_end):
                c_access = 1
            else:
                c_access = 0

            country_data_list.append([e, e + time_interval, c_access])

            e += time_interval

        g = (country_data_list[len(country_data_list) - 1][1])
        while (g >= country_end) and (g <= end_second_interval-5) and (i >= len(country_access_summary) - 1):
            c_access = 0
            country_data_list.append([g, g + time_interval, c_access])
            g += time_interval

    # Returns the list of country/countries in boolean form at time intervals of x seconds and returns\
    # the summary of all countries visible.
    # Country data list in the form of start, end, and 1/0 based on visibility of a country.
    # Country access summary is in the form of start, end, duration and whether land is visible.
    return country_data_list, country_access_summary
