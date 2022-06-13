# ------------------Copyright (C) 2022 University of Strathclyde and Author ---------------------------------
# --------------------------------- Author: Cheyenne Powell -------------------------------------------------
# ------------------------- e-mail: cheyenne.powell@strath.ac.uk --------------------------------------------


# This function calls the OR-Tools solver and stores the values of actions determined into a file
# ===========================================================================================================

from __future__ import print_function
from file_recall import file_recall
import numpy as np
import pandas as pd
import os

from ortools.sat.python import cp_model


def CP_solver(b, c, day, shifts, image_mem, downlink_data_rate, process_im_mem, filename, country_data_list, model,
              summary, time_interval, horizon):
    filename1 = filename + str(day) + '/Solver/Optimized_results' + str(day) + '.txt'
    all_actions = range(0, 3)
    list_num = 0

    # Check if the file is empty and the day is 1.
    if not os.path.isfile(filename1) and day == 1:
        print('file: ' + filename1 + ' does not exists')

        file1 = open(filename1, 'w')
        file1.close()

        pics_count = 0
        processed_pics_count = 0
        downloaded_instances = 0
        idle_time = 0

    # Check if the file is empty and the day is greater than 1.
    elif not os.path.isfile(filename1) and day > 1:
        print('file: ' + filename1 + ' does not exists')

        file1 = open(filename1, 'w')
        file1.close()

        day = day - 1
        filename2 = filename + str(day) + '/Solver/Optimized_results' + str(day) + '.txt'
        results_count_coord, pics_count, processed_pics_count, downloaded_instances, idle_time, memory_total, processed_images, pics_taken = file_recall(
            filename2, list_num)

    # Carry over last data stored in table
    else:
        print('file: ' + filename1 + ' exists')
        results_count_coord, pics_count, processed_pics_count, downloaded_instances, idle_time, memory_total, processed_images, pics_taken = file_recall(
            filename1, list_num)

    solver = cp_model.CpSolver()

    solver.parameters.max_time_in_seconds = 5000
    solver.parameters.log_search_progress = True
    solver.parameters.num_search_workers = 6

    status = solver.Solve(model)
    print(status)

    final_list = []
    downlink_count = 0
    icount = 0

    # use extracted last data for the next row in this function 'b' and 'c' are used to separate the data into "chunks"\

    for n in range(b, c):
        if n == horizon - 1:
            s = n - b
            time_interval = time_interval - 1
        elif 0 < n < c:
            s = n - b
        else:
            s = 0
        check_single_action = 0
        for a in all_actions:
            memory_total = solver.Value(summary[s][2])
            pics_taken = solver.Value(summary[s][0]) / 100
            processed_images = solver.Value(summary[s][1]) / 100
            print(a, n, b, s)
            print('shifts', solver.Value(shifts[(a, s)]))
            if solver.Value(shifts[(a, s)]) == 1:

                check_single_action = check_single_action + 1
                if a == 2:
                    downloaded_instances += 1
                if a == 2 and icount <= 1000:
                    downlink_count += 1
                elif icount > 1000:
                    downlink_count = 0
                    icount = 0
                if a == 0:
                    pics_count += 1
                if a == 1:
                    processed_pics_count += 1


                if any(e[3] == n for e in final_list):
                    z = ([e[3] == n for e in final_list])
                    d = [i for i in range(len(z)) if z[i] == True]
                    print(d)
                    for index in sorted(d, reverse=True):
                        del final_list[index]

                    print('pop')
                    if idle_time > 0:
                        idle_time -= 1

                    final_list.append(
                        [country_data_list[n][0], country_data_list[n][0] + time_interval, a, n,
                         memory_total, pics_taken, pics_count, processed_images, processed_pics_count,
                         processed_pics_count / (image_mem / process_im_mem),
                         downloaded_instances, downloaded_instances / (image_mem / downlink_data_rate), downlink_count,
                         downlink_count / (image_mem / downlink_data_rate),
                         idle_time, 'YES'])
                else:
                    print('Action', a, 'works shift', n, 'time start', country_data_list[n][0],
                          'YES')
                    final_list.append(
                        [country_data_list[n][0], country_data_list[n][0] + time_interval, a, n,
                         memory_total, pics_taken, pics_count, processed_images, processed_pics_count,
                         processed_pics_count / (image_mem / process_im_mem),
                         downloaded_instances, downloaded_instances / (image_mem / downlink_data_rate), downlink_count,
                         downlink_count / (image_mem / downlink_data_rate),
                         idle_time, 'YES'])

            elif any(e[3] == n for e in final_list):
                print('Do nothing,jump to next')

            else:
                print('Action', a, 'works shift', n, 'time start', country_data_list[n][0], 'NO')
                idle_time += 1
                final_list.append(
                    [country_data_list[n][0], country_data_list[n][0] + time_interval, a, n, memory_total,
                     pics_taken, pics_count, processed_images, processed_pics_count,
                     processed_pics_count / (image_mem / process_im_mem),
                     downloaded_instances, downloaded_instances / (image_mem / downlink_data_rate), downlink_count,
                     downlink_count / (image_mem / downlink_data_rate),
                     idle_time, 'NO'])

        if check_single_action > 1:
            print('ERROR: more than one action per time step')

    final_list = sorted(final_list, key=lambda x: x[0])
    np.set_printoptions(threshold=np.inf)
    final_list = np.array(final_list)

    with open(filename1, "a+") as file:
        # Move read cursor to the start of file.
        file.seek(0)
        # If file is not empty then append '\n'
        data = file.read(100)
        if len(data) > 0:
            file.write("\n")
        df = pd.DataFrame(final_list)
        file.writelines(df.to_string(header=False, index=False))

    return c
