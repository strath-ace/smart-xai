"""Code sample to demonstrate how to build a NoOverlap constraint."""

from __future__ import print_function
from ortools.sat.python import cp_model
import math, sys
from ortools.constraint_solver import pywrapcp
import datetime as dt
#from SatelliteCoord import Xband_stations, country_access
import SatelliteCoord
from collections import namedtuple
import collections

import itertools
import numpy as np
from datetime import time

import datetime as dt
import re
import pandas as pd



satellite_coordinates = namedtuple("satellite_coordinates", ['index', 'day', 'month' , 'year', 'time', 'latitude',
                                                             'longitude'])
eclipse_summary = namedtuple("eclipse_summary", ['index', 'day', 'month' , 'year', 'start_time', 'stop_time',
                                                 'duration'])
country_vis = namedtuple("country_vis", ['index','Country', 'day', 'month' , 'year', 'start_time', 'stop_time',
                                         'duration'])
station_access = namedtuple("station_access", ['index', 'day', 'month' , 'year', 'start_time', 'stop_time',
                                               'duration'])

num_tasks = 4
num_days = 1
# load position of satellite
path_coord = 'C:/Users/User/Documents/PhD/ESA/Satellite data/Sentinel 2/Sentinel2A/Longitude_Latitude_Altitude/SENTINEL-2A_40697_LLA_Position1.txt'

f_coord = open(path_coord, "r")
line_count_coord = 0
for line in f_coord:
    if line != "\n":
        line_count_coord += 1
f_coord.close()

f_coord = open(path_coord, "r")
# print(line_count)
node_count_coord = line_count_coord
content_coord = f_coord.read()
lines_coord = content_coord.split('\n')


##########   Eclipse times
path_Eclipse = 'C:/Users/User/Documents/PhD/ESA/Satellite data/Sentinel 2/Sentinel2A/SENTINEL-2A_40697_Eclipse_Summary.txt'

f_Eclipse = open(path_Eclipse, "r")

line_count_Eclipse = 0
for line in f_Eclipse:
    if line != "\n":
        line_count_Eclipse += 1
f_Eclipse.close()

f_Eclipse = open(path_Eclipse, "r")
# print(line_count)
node_count_eclipse = line_count_Eclipse
content_eclipse = f_Eclipse.read()
lines_eclipse = content_eclipse.split('\n')



# Visual of countries
path_country = 'C:/Users/User/Documents/PhD/ESA/Satellite data/Sentinel 2/Sentinel2A/Land Coverage/all countries2.txt'
f_country = open(path_country, "r")

line_count_country = 0
for line in f_country:
    if line != "\n":
        line_count_country += 1
f_country.close()

f_country = open(path_country, "r")
# print(line_count)
node_count_country = line_count_country
content_country = f_country.read()
lines_country = content_country.split('\n')



# Xband to ground stations
path_station = 'C:/Users/User/Documents/PhD/ESA/Satellite data/Sentinel 2/Sentinel2A/X-band Visibility/Facility-EUMETSAT_Maspalomas-To-Satellite-Satellite-Sensor-XBand_Access.txt'
f_station = open(path_station, "r")
content_station = f_station.read()
lines_station = content_station.split('\n')

time_second_interval = dt.datetime.strptime('00:00:01.00','%H:%M:%S.%f') - dt.datetime(1900,1,1)


def sat_coordinates(day, month, year):
    satellite_coord =[]
    satellite_coord_summary =[]
    #for i in range (6,node_count+1):
    for i in range(6, node_count_coord + 1):

        line_details = lines_coord[i].split()
        satellite_coord.append(satellite_coordinates(i-6,int(line_details[0]),str(line_details[1]),int(line_details[2]),
                                                     str(line_details[3]),float(line_details[4]),float(line_details[5])))

    #print(satellite_coord)
    for i in range (0,len(satellite_coord)):
        #print(satellite_coord[i].latitude,satellite_coord[i].longitude)
        if satellite_coord[i].day == day and satellite_coord[i].month == month and satellite_coord[i].year == year:
            satellite_coord_summary.append([satellite_coord[i].time,satellite_coord[i].latitude,satellite_coord[i].longitude,'Satellite Coordinates'])
    return satellite_coord_summary


def eclipse (day,month, year):


    eclipse_sum =[]
    eclipse_final =[]
    #for i in range (6,node_count_eclipse+1):
    for i in range(6, node_count_eclipse + 1):
        # print(i)

        line_details_eclipse = lines_eclipse[i].split()
        if line_details_eclipse[10] == 'Moon':
            eclipse_sum.append(eclipse_summary(i - 6, int(line_details_eclipse[0]), str(line_details_eclipse[1]),
                                               int(line_details_eclipse[2]), str(line_details_eclipse[3]),
                                               str(line_details_eclipse[9]), float(line_details_eclipse[11])))
        else:
            eclipse_sum.append(eclipse_summary(i - 6, int(line_details_eclipse[0]), str(line_details_eclipse[1]),
                                               int(line_details_eclipse[2]), str(line_details_eclipse[3]),
                                               str(line_details_eclipse[15]), float(line_details_eclipse[17])))
    for i in range(0, len(eclipse_sum)):
        if eclipse_sum[i].day == day and eclipse_sum[i].month == month and eclipse_sum[i].year == year:
            eclipse_final.append([eclipse_sum[i].start_time, eclipse_sum[i].stop_time, eclipse_sum[i].duration, 'Penumbra Shade'])
    return eclipse_final


def country_access(day, month, year, country):

    country_accesses = []
    country_access_summary = []
    for i in range (6,node_count_country+1):
    #for i in range(6, 8 + 1):
        #print(i)
        line_details_country = lines_country[i].split()
        country_accesses.append(country_vis(i - 6, str(line_details_country[0]), int(line_details_country[1]),
                                           str(line_details_country[2]), int(line_details_country[3]),
                                           str(line_details_country[4]), str(line_details_country[8]),
                                          float(line_details_country[9])))
        #print(country_access)

    for i in range (0,len(country_accesses)):
        if country == 'All'or country == '':
            if country_accesses[i].day == day and country_accesses[i].month == month and country_accesses[
                i].year == year:
                country_access_summary.append(
                    [country_accesses[i].start_time, country_accesses[i].stop_time, country_accesses[i].duration,
                     country_accesses[i].Country])
        else:
            if country_accesses[i].day == day and country_accesses[i].month == month and country_accesses[i].year == year and country_accesses[i].Country == country:
                country_access_summary.append([country_accesses[i].start_time,country_accesses[i].stop_time,country_accesses[i].duration,country_accesses[i].Country])
    return country_access_summary



def Xband_stations (day,month,year):

    station_accesses = []
    station_accesses1 = []
    station_accesses2 = []
    station_accesses3 = []
    stations_summary = []
    Xband = 'Eumetsat'

    #for a in range (0,4):
    for a in range(0, 4):
        # while Xband != '':
        #print(a)
        if Xband == 'Eumetsat':

            for i in range(8, 857 + 1):
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
                                             station_accesses[i].duration,Xband])

            Xband = 'Matera'
            a += 1
            #return stations_summary

        else:
            if Xband == 'Matera':
                i = 874
                for i in range(876, 1917 + 1):
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
                            [ station_accesses1[i].start_time, station_accesses1[i].stop_time,
                             station_accesses1[
                                 i].duration,Xband])
                Xband = 'PrudhoeBay'
                a += 1
                #return stations_summary

            else:
                if Xband == 'PrudhoeBay':
                    i = 1928
                    for i in range(1929, 4096 + 1):
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
                                [station_accesses2[i].start_time, station_accesses2[i].stop_time,station_accesses2[
                                     i].duration,Xband])
                    Xband = 'Svalbard'
                    a += 1
                    #return stations_summary

                else:
                    if Xband == 'Svalbard':
                        i = 4107
                        for i in range(4108, 6510 + 1):
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
                                    [station_accesses3[i].start_time, station_accesses3[i].stop_time,station_accesses3[
                                         i].duration,Xband])
                        Xband = ''
                        a += 1
                        return stations_summary

                    else:

                        print('Error no data found')

        #######Extract time, lat and long for the satellite during respective days
    #.........idle time
def processing_time(day, month, year,country):
    idle_time =[]
    Total_Table = []
    Total_Table.append([country_access(day,month,year,country)+Xband_stations(day,month,year)+eclipse(day,month,year)])
    Total_Table = list(itertools.chain.from_iterable(list(itertools.chain.from_iterable(Total_Table))))
    sort_list = sorted(Total_Table, key=lambda x: x[0])
    np.set_printoptions(threshold=np.inf)
    Total_Table = np.array(sort_list)
    #print(Total_Table)
    for a in range(0, len(Total_Table)):
        Start_time = Total_Table[a][0]
        End_Time = Total_Table[a][1]
        #print(Start_time)
        #print(End_Time)
        for b in range(a, len(Total_Table)-1):
            if Total_Table[b][0] >= Total_Table[b-1][1]:
                #print('first address',Total_Table[b+1][0])
                Satellite_status = 'Process_images'

                idle_start_time = (dt.datetime.strptime(Total_Table[b-1][1],'%H:%M:%S.%f') - dt.datetime(1900,1,1))+time_second_interval
                idle_end_time = (dt.datetime.strptime(Total_Table[b][0],'%H:%M:%S.%f') - dt.datetime(1900,1,1))-time_second_interval

                idle_duration = idle_end_time - idle_start_time

                if idle_duration >= time_second_interval*60:

                    #idle_time.append([str(idle_start_time)[:-3],str(idle_end_time)[:-3],str(idle_duration)[:-3], Satellite_status])
                    idle_time.append([str(idle_start_time)[:-3], str(idle_end_time)[:-3], str(idle_duration.total_seconds()), Satellite_status])

        return idle_time


#if __name__ == '__main__':
def main():


    occurence_list=[]
    import sys

    if len(sys.argv) >= 1:

        day =1
        month = 'Dec'
        year = 2020
        country = 'United_Kingdom_8'
        #print(Xband_stations(day,month,year))
        max_length = max(country_access(day,month,year,country),eclipse(day,month,year),Xband_stations(day,month,year))
        #print(len(max_length))
        #for i in (0, len(max_length)):
        occurence_list.append([country_access(day,month,year,country)+Xband_stations(day,month,year)+eclipse(day,month,year),processing_time(day,month,year,country)])
        occurence_list = list(itertools.chain.from_iterable(list(itertools.chain.from_iterable(occurence_list))))


        sorted_list = sorted(occurence_list, key=lambda x: x[0])
        np.set_printoptions(threshold=np.inf)
        occurence_list= np.array(sorted_list)

        model = cp_model.CpModel()

        jobs_data = []

        #assign integer values to condition situations
        a = 0
        job_action = 0
        # assign integer values to condition situations
        while a < len(occurence_list):

            prenum_repeat = 1

            if occurence_list[a][3] == 'Penumbra Shade':

                penumbra_starttime = occurence_list[a][0]
                penumbra_endtime = occurence_list[a][1]

                start_time = occurence_list[a][0]
                end_time = occurence_list[a][1]
                duration = occurence_list[a][2]
                job_action = 5
                #jobs_data.append([job_action, start_time, end_time, duration])

                for z in range(a, len(occurence_list)):

                    if occurence_list[z][0] >= penumbra_starttime and occurence_list[z][0] <= penumbra_endtime and any(
                            e[3] == occurence_list[z][3] for e in Xband_stations(day, month, year)):
                        start_time = occurence_list[z][0]
                        end_time = occurence_list[z][1]
                        duration = occurence_list[z][2]
                        job_action = 4
                        jobs_data.append([job_action, start_time, end_time, duration])
                        prenum_repeat = 0
                        a = z


                    elif occurence_list[z][0] >= penumbra_starttime and occurence_list[z][
                        0] <= penumbra_endtime and any(
                            e[3] == occurence_list[z][3] for e in country_access(day, month, year, country)):
                        start_time = occurence_list[z][0]
                        end_time = occurence_list[z][1]
                        duration = occurence_list[z][2]
                        job_action = 0
                        prenum_repeat = 0
                        jobs_data.append([job_action, start_time, end_time, duration])
                        a = z

                    elif occurence_list[z][0] >= penumbra_starttime and occurence_list[z][0] <= penumbra_endtime and \
                            occurence_list[z][3] == 'Process_images':
                        start_time = occurence_list[z][0]
                        end_time = occurence_list[z][1]
                        duration = occurence_list[z][2]
                        job_action = 2
                        prenum_repeat = 0
                        jobs_data.append([job_action, start_time, end_time, duration])
                        a = z


            elif any(e[3] == occurence_list[a][3] for e in Xband_stations(day, month, year)) and (prenum_repeat == 1):
                start_time = occurence_list[a][0]
                end_time = occurence_list[a][1]
                duration = occurence_list[a][2]
                job_action = 4


            elif any(e[3] == occurence_list[a][3] for e in country_access(day, month, year, country)) and (
                    job_action != 0) and (prenum_repeat == 1):
                start_time = occurence_list[a][0]
                end_time = occurence_list[a][1]
                duration = occurence_list[a][2]
                job_action = 1

            elif occurence_list[a][3] == 'Process_images' and (prenum_repeat == 1):
                start_time = occurence_list[a][0]
                end_time = occurence_list[a][1]
                duration = occurence_list[a][2]
                job_action = 2

            else:
                start_time = occurence_list[a][0]
                end_time = occurence_list[a][1]
                duration = occurence_list[a][2]
                job_action = 3

            if prenum_repeat == 1 and job_action!=5:
                jobs_data.append([job_action, start_time, end_time, duration])
            # prenum_repeat = 1
            a += 1

        # jobs_data = list(itertools.chain.from_iterable(list(itertools.chain.from_iterable(jobs_data))))

        # sorted_list2 = sorted(jobs_data, key=lambda x: x[0])
        # np.set_printoptions(threshold=np.inf)
        jobs_data = np.array(jobs_data)
        print(occurence_list)
        print(jobs_data)

        # total memory onboard

        end_jobs =[]
        start_jobs = []
        duration_vars=[]
        all_tasks = {}
        weight = []
        j_tasks =[]
        total_mem = []
        onboard_mem = 2.4 * 10 ** 12
        jobs_model_list=collections.defaultdict(list)
        task_type = collections.namedtuple('task_type', 'start job_task end interval')

        #initialize variables
        for task in range (0,len(jobs_data)):

            #total memory onboard memory allocation

            start_variables = int(((dt.datetime.strptime(str(jobs_data[task][1]),'%H:%M:%S.%f') - dt.datetime(1900,1,1)).total_seconds())*1000)
            end_variables =  int(((dt.datetime.strptime(str(jobs_data[task][2]),'%H:%M:%S.%f') - dt.datetime(1900,1,1)).total_seconds())*1000)
            suffix = '_%i' % (task)
            start_var = model.NewIntVar(start_variables,end_variables-1, 'start'+suffix)
            end_var = model.NewIntVar(start_variables+1, end_variables,'end' + suffix)
            duration_var = model.NewIntVar(0,int(float(jobs_data[task][3])*1000),'duration' + suffix)
            interval_var = model.NewIntervalVar(start_var, duration_var, end_var, 'task' + suffix)

            if jobs_data[task][0]=='1':
                weights = 3
            elif jobs_data[task][0]=='4':
                weights = 2
            elif jobs_data[task][0]=='0':
                weights = 0
            else:
                weights = 1




            all_tasks[task] = task_type(start=start_var, job_task=(jobs_data[task][0]), end=end_var,interval=interval_var)
            jobs_model_list[task].append(interval_var)
            j_tasks.append(jobs_data[task][0])
            weight.append(weights)
            end_jobs.append(end_var)
            start_jobs.append(start_var)
            duration_vars.append(duration_var)
        #print(weight)



        for task in range(0, len(jobs_data) - 1):
            model.Add(all_tasks[task+ 1].start >= all_tasks[task].end)


        #model.AddDecisionStrategy([start_jobs[jobs] for jobs in range (0,len(jobs_data))], cp_model.CHOOSE_FIRST,cp_model.SELECT_MIN_VALUE)

        model.Maximize(sum((weight[task] * duration_vars[task]) for task in range(0, len(jobs_data))))

        boolean_list = []
        w = [model.NewBoolVar('w_%i' % v) for v in range(0, len(jobs_data))]
        x = [model.NewBoolVar('x_%i' % v) for v in range(0, len(jobs_data))]
        y = [model.NewBoolVar('y_%i' % v) for v in range(0, len(jobs_data))]
        z = [model.NewBoolVar('z_%i' % v) for v in range(0, len(jobs_data))]

        for i in range(0, len(jobs_data)):

            f = model.NewIntVar(int(all_tasks[i].job_task), int(all_tasks[i].job_task), 'f')


            model.Add(f == 1).OnlyEnforceIf(w[i])
            model.Add(f != 1).OnlyEnforceIf(w[i].Not())
            model.Add(f == 2).OnlyEnforceIf(x[i])
            model.Add(f != 2).OnlyEnforceIf(x[i].Not())
            model.Add(f == 3).OnlyEnforceIf(y[i])
            model.Add(f != 3).OnlyEnforceIf(y[i].Not())
            model.Add(f == 4).OnlyEnforceIf(z[i])
            model.Add(f != 4).OnlyEnforceIf(z[i].Not())
            boolean_list.append([f, w, x, y, z])




        solver = cp_model.CpSolver()
        status = solver.Solve(model)
        #print(model)

        solver.parameters.search_branching = cp_model.FIXED_SEARCH

        final_start =[]
        final_end =[]
        final_duration = []
        final_jobs = []

        if status == cp_model.OPTIMAL:
        # Print out makespan and the start times for all tasks.
            print('Optimal Schedule Length: %i' % solver.ObjectiveValue())
            for jobs in jobs_model_list:
                #print('Job',jobs,' starts at %i' % solver.Value(start_jobs[jobs]),' ends at %i' % solver.Value(end_jobs[jobs]),' duration is %i' % solver.Value(duration_vars[jobs]))

                #convert micro seconds to time hh mm ss
                start = str(dt.timedelta(seconds=((solver.Value(start_jobs[jobs]))/1000)))[:-3]
                end = str(dt.timedelta(seconds=((solver.Value(end_jobs[jobs]))/1000)))[:-3]
                duration = (solver.Value(duration_vars[jobs]))/1000
                final_jobs = (all_tasks[jobs].job_task)
                print('Job',jobs,' starts at ', start,' ends at ',end,' duration is ',duration,' job task: ',final_jobs, '[',solver.Value(w[jobs]),solver.Value(x[jobs]),solver.Value(y[jobs]),solver.Value(z[jobs]),']')

                # print('Job',jobs,' ends at %i' % solver.Value(end_jobs[jobs]))
                # print('Job',jobs,' duration is %i' % solver.Value(duration_vars[jobs]))
                # print(' job task %i' % solver.Value(all_tasks[jobs].job_task)')


        else:
            print('Solver exited with nonoptimal status: %i' % status)




      # Solve model.



main()