from __future__ import print_function
from ortools.sat.python import cp_model
import os


def CPModel_data(interval,onboard_mem, image_mem, downlink_data_rate, process_im_mem, filename, mem_data_list, country_data_list,
                 gnd_data_list, day_data_list, horizon):
    all_actions = range(0, 3)
    if not os.path.isfile(filename):
        print('file: ' + filename + ' does not exists')
        memory_keep = []
        processed_keep = []
        photos_keep = []

        num_processed = 0
        num_pics = 0
        memory = 0

        c = 0

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
        memory = results_data[4]
        num_pics = int(results_data[5] * 100)
        num_processed = int(results_data[7] * 100)

        memory_keep = [memory]
        processed_keep = [num_processed]
        photos_keep = [num_pics]

        c = results_count_coord

    hot_start = 1
    summary = []
    # at start b and c are the same
    b = c
    # j = remainder of division
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
    shifts = {}
    for s in mod_shifts:

        for a in all_actions:
            shifts[(a, s)] = model.NewBoolVar('shift_a%is%i' % (a, s))

    for s in mod_shifts:
        model.Add(sum(shifts[(a, s)] for a in all_actions) <= 1)

    # for a in all_actions:
    for n in all_shifts:
        # print('n',n)
        if n > 0:
            s = n - b
            # print('s',s)
        else:
            s = 0
        # for a in all_actions:

        model.Add(((country_data_list[n][2] == day_data_list[n][2]) and (
                country_data_list[n][2] == 1))).OnlyEnforceIf(shifts[(0, s)])

        model.Add(gnd_data_list[n][2] == 1).OnlyEnforceIf(shifts[(2, s)])

    for s in mod_shifts:

        # for a in all_actions :
        #
        if len(memory_keep) >= 1 and s == 0:
            num_pics = int(photos_keep[len(photos_keep) - 1])
            print(num_pics)
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

    model.Maximize(sum((shifts[(2, s)]) + shifts[(0, s)] + shifts[(1, s)] for s in mod_shifts))

    if hot_start == 1:
        # import first guess

        # manual_request = np.zeros((3, horizon))
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

    return model, summary, shifts,b
