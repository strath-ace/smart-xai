from __future__ import print_function
import numpy as np
import pandas as pd
import os

from ortools.sat.python import cp_model


def CP_solver(b, c, shifts, image_mem, downlink_data_rate, process_im_mem, filename, country_data_list, model, summary, time_interval):
    all_actions = range(0, 3)
    if not os.path.isfile(filename):
        print('file: ' + filename + ' does not exists')

        file1 = open(filename, 'w')
        file1.close()

        pics_count = 0
        processed_pics_count = 0
        downloaded_instances = 0
        idle_time = 0
        memory_total = 0
        processed_images = 0
        pics_taken = 0


    else:
        print('file: ' + filename + ' exists')
        results_coord = open(filename, "r")
        results_count_coord = 0
        for line in results_coord:
            if line != "\n":
                results_count_coord += 1
        results_coord.close()
        results_coord = open(filename, "r")
        # print(results_count)
        results_count_coord = results_count_coord
        results_coord = results_coord.read()
        results_coord = results_coord.split('\n')
        results_data = results_coord[results_count_coord - 1].split()

        # Carry over last data stored in table
        pics_count = int(results_data[6])
        processed_pics_count = int(results_data[8])
        downloaded_instances = int(results_data[10])
        idle_time = int(results_data[12])

        memory_total = int(results_data[4])
        processed_images = int(float(results_data[7]) * 100)
        pics_taken = int(float(results_data[5]) * 100)


    solver = cp_model.CpSolver()

    # solver.parameters.search_branching = cp_model.LP_SEARCH
    solver.parameters.max_time_in_seconds = 5000
    solver.parameters.log_search_progress = True
    solver.parameters.num_search_workers = 8

    status = solver.Solve(model)
    print(status)

    final_list = []
    downlink_count = 0
    icount =0
    for n in range(b, c):
        if 0 < n < c:
            s = n - b
        elif n == c:
            s = n - b
            time_interval = time_interval - 1
        else:
            s = 0
        check_single_action = 0
        for a in all_actions:

            print(a, n, b, s)
            print('shifts', solver.Value(shifts[(a, s)]))
            if solver.Value(shifts[(a, s)]) == 1:
                memory_total = solver.Value(summary[s][2])
                pics_taken = solver.Value(summary[s][0]) / 100
                processed_images = solver.Value(summary[s][1]) / 100
                check_single_action = check_single_action + 1
                if a == 2:
                    downloaded_instances += 1
                if a == 2 and icount <=1000:
                    downlink_count += 1
                elif icount > 1000:
                    downlink_count = 0
                    icount = 0
                if a == 0:
                    pics_count += 1
                if a == 1:
                    processed_pics_count += 1
                # print('Action', a, 'works shift', n, 'time start', country_data_list[n][0])

                if any(e[3] == n for e in final_list):
                    z = [i for i, lst in enumerate(final_list) if n in lst][0]
                    # print('Removing Action', a, 'works shift', n, 'time start', country_data_list[n][0],
                    #      'NO')
                    # print('pop')
                    # print('Adding Action', a, 'works shift', n, 'time start', country_data_list[n][0],
                    #      'YES')
                    final_list.pop(z)
                    # print('Action', a, 'works shift', n, 'time start', country_data_list[n][0])  # ,summary[s][0],summary[s][1])
                    final_list.append(
                        [country_data_list[n][0], country_data_list[n][0] + time_interval, a, n,
                         memory_total, pics_taken, pics_count, processed_images, processed_pics_count,
                         processed_pics_count / (image_mem / process_im_mem),
                         downloaded_instances, downloaded_instances / (image_mem / downlink_data_rate),downlink_count,downlink_count/ (image_mem / downlink_data_rate),
                         idle_time, 'YES'])
                else:
                    print('Action', a, 'works shift', n, 'time start', country_data_list[n][0],
                          'YES')
                    final_list.append(
                        [country_data_list[n][0], country_data_list[n][0] + time_interval, a, n,
                         memory_total, pics_taken, pics_count, processed_images, processed_pics_count,
                         processed_pics_count / (image_mem / process_im_mem),
                         downloaded_instances, downloaded_instances / (image_mem / downlink_data_rate),downlink_count,downlink_count/ (image_mem / downlink_data_rate),
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
                     downloaded_instances, downloaded_instances / (image_mem / downlink_data_rate),downlink_count,downlink_count/ (image_mem / downlink_data_rate),
                     idle_time, 'NO'])

        if check_single_action > 1:
            print('ERROR: more than one action per time step')
            # combined_lists=final_list
            # combined_lists.append([final_list1])
    #print(final_list)
    final_list = sorted(final_list, key=lambda x: x[0])
    np.set_printoptions(threshold=np.inf)
    final_list = np.array(final_list)

    with open(filename, "a+") as file:
        # Move read cursor to the start of file.
        file.seek(0)
        # If file is not empty then append '\n'
        data = file.read(100)
        if len(data) > 0:
            file.write("\n")
        df = pd.DataFrame(final_list)
        file.writelines(df.to_string(header=False, index=False))

    return c
    # return memory_total, processed_images, pics_taken
