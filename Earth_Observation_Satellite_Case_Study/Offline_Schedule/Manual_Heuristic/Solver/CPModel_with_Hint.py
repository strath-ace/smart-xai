# This file contains the or-tools model and hints a solution from the manual schedule created

from __future__ import print_function
from ortools.sat.python import cp_model
from file_recall import file_recall
import os


def CPModel_data(day, interval, onboard_mem, image_mem, downlink_data_rate, process_im_mem, filename, mem_data_list, country_data_list,
                 gnd_data_list, day_data_list, horizon):
    all_actions = range(0, 3)
    filename1 = filename + str(day) + '/Solver/Optimized_results' + str(day) + '.txt'
    list_num = 1
    if not os.path.isfile(filename1) and day == 1:
        print('file: ' + filename1 + ' does not exists')
        memory_keep = []
        processed_keep = []
        photos_keep = []
        num_processed = 0
        num_pics = 0
        memory = 0
        c = 0

    elif not os.path.isfile(filename1) and day > 1:
        print('file: ' + filename1 + ' does not exists')
        day = day - 1
        filename2 = filename + str(day) + '/Solver/Optimized_results' + str(day) + '.txt'
        results_count_coord, memory, num_pics, num_processed, memory_keep, processed_keep, photos_keep = file_recall(filename2, list_num)
        c = 0
    else:
        print('file: ' + filename1 + ' exists')
        results_count_coord, memory, num_pics, num_processed, memory_keep, processed_keep, photos_keep = file_recall(filename1, list_num)
        c = results_count_coord

    hot_start = 1
    summary = []
    # at start b and c are the same
    b = c
    # j is the remainder of division
    j = horizon % interval
    # check the division to determine loops (reps)
    if j > 0 and ((b + j) == horizon):
        c = b + j
    else:
        c = b + int(horizon / (horizon / interval))

    print(b, c)
    all_shifts = range(b, c)
    mod_shifts = range(0, c - b)

    model = cp_model.CpModel()

    # shifts[(a,s)] is used to determine the action with the respective shift, in this case 3 actions - take images '0', process '1' and downlink '2'
    shifts = {}
    for s in mod_shifts:

        for a in all_actions:
            shifts[(a, s)] = model.NewBoolVar('shift_a%is%i' % (a, s))

    # no more than 1 action can be executed per shift, also meaning no actions can be executed
    for s in mod_shifts:
        model.Add(sum(shifts[(a, s)] for a in all_actions) <= 1)

    for n in all_shifts:

        if n > 0:
            s = n - b
        else:
            s = 0

        # initialises the actions based on the occurrences from the satellite schedule over a period of a day
        # meaning action '0' - take images, can only occur (has a boolean variable of 1) when the country/land is seen during the day (sunlight-exposure)
        # (country_data_list[n][2] == day_data_list[n][2]) can also be a '1' if both are '0' thus the 2 'and' statements are needed
        model.Add(((country_data_list[n][2] == day_data_list[n][2]) and (
                country_data_list[n][2] == 1))).OnlyEnforceIf(shifts[(0, s)])

        # action '2' - downlink is assigned a boolean value of '1' when ground station is accessible at any time over a day period
        model.Add(gnd_data_list[n][2] == 1).OnlyEnforceIf(shifts[(2, s)])

    # constraints are applied here, based on the calculations, float values are created that the model is unable to handle, therefore
    # multiples of 100 are used.
    # The constraints here means an image has to be taken first and once taken, processing can occur at any time, followed by downlinking based on the images processed
    # The images taken are kept in memory when processing has occurred until they are downlinked, hen an equivalent amount is deleted
    # however 1 process instance is  0.0927 of an image so processing has to occur at least 11 times for an image to be completed
    # Note, this is based on the hardware capabilities of the satellite that can be altered in the solver_test file
    # equations are as follows: number of process instance required = (num_pics * int((image_mem / process_im_mem)
    #                           number of downlinked instance required = (int(processed images * process_im_mem/ downlink_data_rate )
    for s in mod_shifts:

        if len(memory_keep) >= 1 and s == 0:
            num_pics = int(photos_keep[len(photos_keep) - 1])
            memory = memory_keep[len(memory_keep) - 1]
            num_processed = int(processed_keep[len(processed_keep) - 1])

            num_pics = num_pics + (shifts[(0, s)] * 100) - (
                    shifts[(2, s)] * (int(100 * downlink_data_rate / image_mem)))
            memory = memory + (image_mem * (shifts[(0, s)])) + (process_im_mem * shifts[(1, s)]) - (
                    2 * downlink_data_rate * (shifts[(2, s)]))
            num_processed = num_processed + (shifts[(1, s)] * 100) - (
                    shifts[(2, s)] * (int(100 * downlink_data_rate / process_im_mem)))
        else:
            num_pics += (shifts[(0, s)] * 100) - (shifts[(2, s)] * (int(100 * downlink_data_rate / image_mem)))
            memory += (image_mem * (shifts[(0, s)])) + (process_im_mem * shifts[(1, s)]) - (
                    2 * downlink_data_rate * (shifts[(2, s)]))
            num_processed += (shifts[(1, s)] * 100) - (
                    shifts[(2, s)] * (int(100 * downlink_data_rate / process_im_mem)))

        model.Add(num_processed > (int(100 * downlink_data_rate / process_im_mem))).OnlyEnforceIf(
            shifts[(2, s)])
        model.Add(num_pics > 0).OnlyEnforceIf(shifts[(1, s)])
        total_to_process = (num_pics * int((image_mem / process_im_mem)))
        model.Add(num_processed <= total_to_process)
        model.Add(memory < onboard_mem)
        summary.append([num_pics, num_processed, memory])

    # the objective function is to maximize the occurrences of images taken, processed and downlinked. Can be altered
    # shifts[(2, s)] = downlink, shifts[(1, s)] = process, shifts[(0, s)] = pics
    # model.Maximize(sum((shifts[(2, s)]) + shifts[(0, s)] + shifts[(1, s)] for s in mod_shifts))
    # model.Maximize(sum((shifts[(2, s)]) + shifts[(0, s)] for s in mod_shifts))
    model.Maximize(sum((shifts[(2, s)]) for s in mod_shifts))
    # manual schedule inputted here as a hint to the solution
    if hot_start == 1:

        for n in all_shifts:
            if n > 0:
                s = n - b
            else:
                s = 0

            if mem_data_list[n][2] == 0:
                model.AddHint(shifts[(0, s)], 1)
            if mem_data_list[n][2] == 1:
                model.AddHint(shifts[(1, s)], 1)
            if mem_data_list[n][2] == 2:
                model.AddHint(shifts[(2, s)], 1)
    # returns the overall model to the solver, the summary table, shifts, the start and end time for the loop (intervals) can be altered
    return model, summary, shifts, b, c
