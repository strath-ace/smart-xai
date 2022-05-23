# Function for generating the schedule-
# 1 prevents images from being taken when in the shade
# 2 where actions overlap  a weight is given to the actions to prioritise 1 over the other, thus durations for the lower prioritised action is altered
# Finally, generates the final schedule

import collections
import datetime as dt
import itertools
import numpy as np
import pandas as pd

from ortools.sat.python import cp_model
from collections import namedtuple
from Earth_Observation_Satellite_Case_Study.Offline_Schedule.Manual_Heuristic.Manually_created_schedule.Manual_Processing_Time import processing_time

satellite_coordinates = namedtuple("satellite_coordinates", ['index', 'day', 'month', 'year', 'time', 'latitude',
                                                             'longitude'])
eclipse_summary = namedtuple("eclipse_summary", ['index', 'day', 'month', 'year', 'start_time', 'stop_time',
                                                 'duration'])
country_vis = namedtuple("country_vis", ['index', 'Country', 'day', 'month', 'year', 'start_time', 'stop_time',
                                         'duration'])
station_access = namedtuple("station_access", ['index', 'day', 'month', 'year', 'start_time', 'stop_time',
                                               'duration'])


# function for task determination
def task_decision(day, occurrence_list, stations_summary, country_access_summary, file2):
    jobs_data = []

    # assign integer values to condition situations
    a = 0
    # job action = 0 -> idle
    # job action = 1 -> take images
    # job action = 2 -> processing
    # job action = 3 -> calibrate
    # job action = 4 -> downlink images
    # assign integer values to condition situations
    while a < len(occurrence_list):

        start_time = (int(((dt.datetime.strptime(str(occurrence_list[a][0]), '%H:%M:%S.%f') - dt.datetime(1900, 1, 1)).total_seconds())))
        end_time = (int(((dt.datetime.strptime(str(occurrence_list[a][1]), '%H:%M:%S.%f') - dt.datetime(1900, 1, 1)).total_seconds())))

        prenum_repeat = 1
        # check to see if land is in night and removes options for pictures to be taken and replaces it with processing
        if occurrence_list[a][3] == 'Penumbra Shade':

            penumbra_starttime = (int(((dt.datetime.strptime(str(occurrence_list[a][0]), '%H:%M:%S.%f') - dt.datetime(1900, 1, 1)).total_seconds())))
            penumbra_endtime = (int(((dt.datetime.strptime(str(occurrence_list[a][1]), '%H:%M:%S.%f') - dt.datetime(1900, 1, 1)).total_seconds())))

            for z in range(a, len(occurrence_list)):
                start_time = (int(((dt.datetime.strptime(str(occurrence_list[z][0]), '%H:%M:%S.%f') - dt.datetime(1900, 1, 1)).total_seconds())))
                end_time = (int(((dt.datetime.strptime(str(occurrence_list[z][1]), '%H:%M:%S.%f') - dt.datetime(1900, 1, 1)).total_seconds())))

                if penumbra_starttime <= start_time <= penumbra_endtime and any(
                        e[3] == occurrence_list[z][3] for e in stations_summary) and (start_time < end_time):
                    start_time = occurrence_list[z][0]
                    end_time = occurrence_list[z][1]
                    duration = occurrence_list[z][2]
                    job_action = 4
                    jobs_data.append([job_action, start_time, end_time, duration])
                    a = z

                # if country is seen at night
                elif penumbra_starttime <= start_time <= penumbra_endtime and any(e[3] == occurrence_list[z][3] for e in country_access_summary) and \
                        (start_time < end_time):
                    start_time = occurrence_list[z][0]
                    end_time = occurrence_list[z][1]
                    duration = occurrence_list[z][2]
                    job_action = 2
                    jobs_data.append([job_action, start_time, end_time, duration])
                    a = z

                elif penumbra_starttime <= start_time <= penumbra_endtime and \
                        occurrence_list[z][3] == 'Process_images' and (start_time < end_time):
                    start_time = occurrence_list[z][0]
                    end_time = occurrence_list[z][1]
                    duration = occurrence_list[z][2]
                    job_action = 2
                    jobs_data.append([job_action, start_time, end_time, duration])
                    a = z

        elif any(e[3] == str(occurrence_list[a][3]) for e in stations_summary) and (prenum_repeat == 1) and (start_time < end_time):
            start_time = occurrence_list[a][0]
            end_time = occurrence_list[a][1]
            duration = occurrence_list[a][2]
            job_action = 4
            jobs_data.append([job_action, start_time, end_time, duration])

        elif any(e[3] == str(occurrence_list[a][3]) for e in country_access_summary) and (prenum_repeat == 1) and (start_time < end_time):
            start_time = occurrence_list[a][0]
            end_time = occurrence_list[a][1]
            duration = occurrence_list[a][2]
            job_action = 1
            jobs_data.append([job_action, start_time, end_time, duration])

        elif occurrence_list[a][3] == 'Process_images' and (prenum_repeat == 1) and (start_time < end_time):
            start_time = occurrence_list[a][0]
            end_time = occurrence_list[a][1]
            duration = occurrence_list[a][2]
            job_action = 2
            jobs_data.append([job_action, start_time, end_time, duration])

        else:

            start_time = occurrence_list[a][0]
            end_time = occurrence_list[a][1]
            duration = occurrence_list[a][2]
            job_action = 2
            jobs_data.append([job_action, start_time, end_time, duration])

        a += 1
    jobs_data = np.array(jobs_data)
    # print(occurrence_list)
    # print(jobs_data)

    df = pd.DataFrame(jobs_data)
    file2.writelines(df.to_string(header=False, index=False))
    file2.close()

    return jobs_data


def heuristic(path, day, month, year, country, time_interval):
    file1 = open(path + str(day) + '/daily_schedule' + str(day) + '.txt', 'w')
    file2 = open(path + str(day) + '/jobs_daily_schedule' + str(day) + '.txt', 'w')
    file3 = open(path + str(day) + '/Manual_Results' + str(day) + '.txt', 'w')

    # processing time function called as processing is manually added  based on the availability of the gaps between actions
    idle_time, Total_Table, country_access_summary, stations_summary, eclipse_final = processing_time(day, month, year, country, time_interval)
    occurrence_list = [Total_Table, idle_time]
    occurrence_list = (list(itertools.chain.from_iterable(occurrence_list)))
    # converts all the times to seconds so they can be sorted
    occurrence_list_revised = []
    for i in range(0, len(occurrence_list)):
        new_list = (dt.datetime.strptime(occurrence_list[i][0], '%H:%M:%S.%f') - dt.datetime(1900, 1, 1))
        new_list = new_list.total_seconds()
        # list is in the order of start time, end time, duration, action
        occurrence_list_revised.append([new_list, occurrence_list[i][1], occurrence_list[i][2], occurrence_list[i][3]])

    # sort list in ascending order with respect to start time
    sorted_list = sorted(occurrence_list_revised, key=lambda x: x[0])

    # convert milliseconds to time hh mm ss
    occurrence_list1 = []
    for i in range(0, len(sorted_list)):
        new_list = str(dt.timedelta(seconds=(sorted_list[i][0])))[:-3]
        # prevents the action from going over to the next day since they are only in hh:mm:ss if action is to take place between 11:59 pm and 00:23 am
        # only let action occur for in the day for 1 minute
        if new_list > '23:00:00.001' and '00:00:00.000' < sorted_list[i][1] < '01:00:00.000':

            sorted_list[i][1] = '23:59:59.000'
            sorted_list[i][2] = (dt.datetime.strptime(sorted_list[i][1], '%H:%M:%S.%f') - dt.datetime(1900, 1, 1)) - (dt.datetime.strptime(new_list, '%H:%M:%S.%f') - dt.datetime(1900, 1, 1))
            sorted_list[i][2] = sorted_list[i][2].total_seconds()
            occurrence_list1.append([new_list, sorted_list[i][1], sorted_list[i][2], sorted_list[i][3]])
        else:

            occurrence_list1.append([new_list, sorted_list[i][1], sorted_list[i][2], sorted_list[i][3]])

    sorted_list = occurrence_list1

    np.set_printoptions(threshold=np.inf)
    occurrence_list = np.array(sorted_list)

    df = pd.DataFrame(occurrence_list)
    file1.writelines(df.to_string(header=False, index=False))
    file1.close()
    print(occurrence_list)
    jobs_data = task_decision(day, occurrence_list, stations_summary, country_access_summary, file2)

    end_jobs = []
    start_jobs = []
    duration_vars = []
    all_tasks = {}
    weight = []
    j_tasks = []

    model = cp_model.CpModel()

    jobs_model_list = collections.defaultdict(list)
    task_type = collections.namedtuple('task_type', 'start job_task end interval')

    # initialize variables and assign weights to task to determine the start and end time of actions if they overlap, the higher the weight, the more the action is prioritised
    for task in range(0, len(jobs_data)):

        # total memory onboard memory allocation
        start_variables = int(((dt.datetime.strptime(str(jobs_data[task][1]), '%H:%M:%S.%f') - dt.datetime(1900, 1, 1)).total_seconds()) * 1000)
        end_variables = int(((dt.datetime.strptime(str(jobs_data[task][2]), '%H:%M:%S.%f') - dt.datetime(1900, 1, 1)).total_seconds()) * 1000)
        suffix = '_%i' % task
        start_var = model.NewIntVar(start_variables, end_variables - 1, 'start' + suffix)
        end_var = model.NewIntVar(start_variables + 1, end_variables, 'end' + suffix)
        duration_var = model.NewIntVar(0, int(float(jobs_data[task][3]) * 1000), 'duration' + suffix)
        interval_var = model.NewIntervalVar(start_var, duration_var, end_var, 'task' + suffix)

        # take 1 picture per x seconds
        if jobs_data[task][0] == '1':
            weights = 1
        # downlink images
        elif jobs_data[task][0] == '4':
            weights = 3
        # process images
        elif jobs_data[task][0] == '2':
            weights = 2
        else:
            weights = 0

        all_tasks[task] = task_type(start=start_var, job_task=(jobs_data[task][0]), end=end_var, interval=interval_var)
        jobs_model_list[task].append(interval_var)
        j_tasks.append(jobs_data[task][0])
        weight.append(weights)
        end_jobs.append(end_var)
        start_jobs.append(start_var)
        duration_vars.append(duration_var)
        # Demands_mem.append(Demands)

    for task in range(0, len(jobs_data) - 1):
        model.Add(all_tasks[task + 1].start >= all_tasks[task].end)

    # objective used to calculate the durations of the actions
    model.Maximize(sum((weight[task] * duration_vars[task]) for task in range(0, len(jobs_data))))

    solver = cp_model.CpSolver()
    solver.Solve(model)

    solver.parameters.search_branching = cp_model.LP_SEARCH
    solver.parameters.num_search_workers = 6
    solver.parameters.max_time_in_seconds = 10

    final_start = []
    final_end = []
    final_duration = []
    final_jobs = []
    print_list = []

    # if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:

    # Print out makespan and the start times for all tasks.
    # print('Optimal Schedule Length: %i' % solver.ObjectiveValue())
    for jobs in jobs_model_list:
        # convert milli seconds to time hh mm ss
        start = solver.Value(start_jobs[jobs])
        end = solver.Value(end_jobs[jobs])
        duration = (solver.Value(duration_vars[jobs]))

        print_list.append([jobs, start, end, duration, all_tasks[jobs].job_task])  # ,solver.Value(w[jobs]),solver.Value(x[jobs]),solver.Value(y[jobs]),solver.Value(z[jobs])])

        final_start.append(start)
        final_end.append(end)
        final_duration.append(duration)
        final_jobs.append(all_tasks[jobs].job_task)

    df = pd.DataFrame(print_list)
    file3.writelines(df.to_string(header=False, index=False))
