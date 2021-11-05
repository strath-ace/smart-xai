import collections
import datetime as dt
import itertools
import numpy as np
import pandas as pd

from ortools.sat.python import cp_model
from collections import namedtuple
from Manual_Processing_Time import processing_time

satellite_coordinates = namedtuple("satellite_coordinates", ['index', 'day', 'month', 'year', 'time', 'latitude',
                                                             'longitude'])
eclipse_summary = namedtuple("eclipse_summary", ['index', 'day', 'month', 'year', 'start_time', 'stop_time',
                                                 'duration'])
country_vis = namedtuple("country_vis", ['index', 'Country', 'day', 'month', 'year', 'start_time', 'stop_time',
                                         'duration'])
station_access = namedtuple("station_access", ['index', 'day', 'month', 'year', 'start_time', 'stop_time',
                                               'duration'])


def heuristic(path, day, month, year, country):
    file1 = open(path + '/daily_schedule' + str(day) + '.txt', 'w')
    file2 = open(path + '/jobs_daily_schedule' + str(day) + '.txt', 'w')
    file3 = open(path + '/Manual_Results' + str(day) + '.txt', 'w')

    idle_time, Total_Table, country_access_summary, stations_summary, eclipse_final = processing_time(day, month, year, country)
    occurence_list = [Total_Table, idle_time]
    occurence_list = (list(itertools.chain.from_iterable(occurence_list)))
    print(occurence_list)
    # print([str(occurence_list[i][0]) for i in range(0,len(occurence_list))])

    occurence_list_revised = []
    for i in range(0, len(occurence_list)):
        new_list = (dt.datetime.strptime(occurence_list[i][0], '%H:%M:%S.%f') - dt.datetime(1900, 1, 1))
        new_list = new_list.total_seconds()
        occurence_list_revised.append([new_list, occurence_list[i][1], occurence_list[i][2], occurence_list[i][3]])

    sorted_list = sorted(occurence_list_revised, key=lambda x: x[0])

    occurence_list1 = []
    for i in range(0, len(sorted_list)):
        new_list = str(dt.timedelta(seconds=(sorted_list[i][0])))[:-3]

        occurence_list1.append([new_list, sorted_list[i][1], sorted_list[i][2], sorted_list[i][3]])

    sorted_list = occurence_list1

    np.set_printoptions(threshold=np.inf)
    occurence_list = np.array(sorted_list)

    df = pd.DataFrame(occurence_list)
    file1.writelines(df.to_string(header=False, index=False))
    file1.close()

    jobs_data = []

    # assign integer values to condition situations
    a = 0
    job_action = 0

    # assign integer values to condition situations
    while a < len(occurence_list):

        prenum_repeat = 1
        # check to see if land is in night and removes options for pictures to be taken
        if occurence_list[a][3] == 'Penumbra Shade':

            penumbra_starttime = occurence_list[a][0]
            penumbra_endtime = occurence_list[a][1]

            start_time = occurence_list[a][0]
            end_time = occurence_list[a][1]
            duration = occurence_list[a][2]
            job_action = 5

            for z in range(a, len(occurence_list)):

                if penumbra_starttime <= occurence_list[z][0] <= penumbra_endtime and any(
                        e[3] == occurence_list[z][3] for e in stations_summary) and (occurence_list[z][0] < occurence_list[z][1]):
                    start_time = occurence_list[z][0]
                    end_time = occurence_list[z][1]
                    duration = occurence_list[z][2]
                    job_action = 4
                    jobs_data.append([job_action, start_time, end_time, duration])
                    prenum_repeat = 0
                    a = z

                # if country is seen at night
                elif penumbra_starttime <= occurence_list[z][0] <= penumbra_endtime and any(e[3] == occurence_list[z][3] for e in country_access_summary) and\
                        (occurence_list[z][0] < occurence_list[z][1]):
                    start_time = occurence_list[z][0]
                    end_time = occurence_list[z][1]
                    duration = occurence_list[z][2]
                    job_action = 2
                    prenum_repeat = 0
                    jobs_data.append([job_action, start_time, end_time, duration])
                    a = z

                elif penumbra_starttime <= occurence_list[z][0] <= penumbra_endtime and \
                        occurence_list[z][3] == 'Process_images' and (occurence_list[z][0] < occurence_list[z][1]):
                    start_time = occurence_list[z][0]
                    end_time = occurence_list[z][1]
                    duration = occurence_list[z][2]
                    job_action = 2
                    prenum_repeat = 0
                    jobs_data.append([job_action, start_time, end_time, duration])
                    a = z

        elif any(e[3] == occurence_list[a][3] for e in stations_summary) and (prenum_repeat == 1) and (occurence_list[a][0] < occurence_list[a][1]):
            start_time = occurence_list[a][0]
            end_time = occurence_list[a][1]
            duration = occurence_list[a][2]
            job_action = 4

        elif any(e[3] == occurence_list[a][3] for e in country_access_summary) and (
                job_action != 0) and (prenum_repeat == 1) and (occurence_list[a][0] < occurence_list[a][1]):
            start_time = occurence_list[a][0]
            end_time = occurence_list[a][1]
            duration = occurence_list[a][2]
            job_action = 1

        elif occurence_list[a][3] == 'Process_images' and (prenum_repeat == 1) and (occurence_list[a][0] < occurence_list[a][1]):
            start_time = occurence_list[a][0]
            end_time = occurence_list[a][1]
            duration = occurence_list[a][2]
            job_action = 2

        else:

            start_time = occurence_list[a][0]
            end_time = occurence_list[a][1]
            duration = occurence_list[a][2]
            job_action = 3

        if prenum_repeat == 1 and job_action != 5 and (occurence_list[a][0] < occurence_list[a][1]):
            jobs_data.append([job_action, start_time, end_time, duration])

        a += 1
    jobs_data = np.array(jobs_data)
    print(occurence_list)
    print(jobs_data)

    df = pd.DataFrame(jobs_data)
    file2.writelines(df.to_string(header=False, index=False))
    file2.close()

    end_jobs = []
    start_jobs = []
    duration_vars = []
    all_tasks = {}
    weight = []
    j_tasks = []

    model = cp_model.CpModel()

    jobs_model_list = collections.defaultdict(list)
    task_type = collections.namedtuple('task_type', 'start job_task end interval')

    # initialize variables
    for task in range(0, len(jobs_data)):

        # total memory onboard memory allocation

        start_variables = int(((dt.datetime.strptime(str(jobs_data[task][1]), '%H:%M:%S.%f') - dt.datetime(1900, 1, 1)).total_seconds()) * 1000)
        end_variables = int(((dt.datetime.strptime(str(jobs_data[task][2]), '%H:%M:%S.%f') - dt.datetime(1900, 1, 1)).total_seconds()) * 1000)
        suffix = '_%i' % task
        start_var = model.NewIntVar(start_variables, end_variables - 1, 'start' + suffix)
        end_var = model.NewIntVar(start_variables + 1, end_variables, 'end' + suffix)
        duration_var = model.NewIntVar(0, int(float(jobs_data[task][3]) * 1000), 'duration' + suffix)
        interval_var = model.NewIntervalVar(start_var, duration_var, end_var, 'task' + suffix)

        # take pictures 1 per second
        if jobs_data[task][0] == '1':
            weights = 2
        # dump images
        elif jobs_data[task][0] == '4':
            weights = 2
        # process images
        elif jobs_data[task][0] == '2':
            weights = 1
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

    # print(weight)

    for task in range(0, len(jobs_data) - 1):
        model.Add(all_tasks[task + 1].start >= all_tasks[task].end)

    model.Maximize(sum((weight[task] * duration_vars[task]) for task in range(0, len(jobs_data))))

    solver = cp_model.CpSolver()
    solver.Solve(model)

    solver.parameters.search_branching = cp_model.LP_SEARCH
    solver.parameters.log_search_progress = True
    solver.parameters.num_search_workers = 6
    solver.parameters.max_time_in_seconds = 10

    final_start = []
    final_end = []
    final_duration = []
    final_jobs = []
    print_list = []

    # if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:

    # Print out makespan and the start times for all tasks.
    print('Optimal Schedule Length: %i' % solver.ObjectiveValue())
    for jobs in jobs_model_list:
        # print('Job',jobs,' starts at %i' % solver.Value(start_jobs[jobs]),' ends at %i' % solver.Value(end_jobs[jobs]),' duration is %i' % solver.Value(duration_vars[jobs]))

        # convert micro seconds to time hh mm ss
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
