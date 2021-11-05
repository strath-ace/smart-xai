


def CPModel (horizon):
    i = 0
    while i in range(0, horizon):
        summary = []
        b = c

        j = horizon % 3000

        if j > 0 and ((b + j) == horizon):
            c = b + j
        else:
            c = b + int(horizon / (horizon / 3000))

        print(b, c)
        all_shifts = range(b, c)
        mod_shifts = range(0, c - b)

        shifts = {}
        for s in mod_shifts:

            for a in all_actions:
                shifts[(a, s)] = model.NewBoolVar('shift_a%is%i' % (a, s))

        for s in mod_shifts:
            model.Add(sum(shifts[(a, s)] for a in all_actions) <= 1)

        # for a in all_actions:
        for n in all_shifts:
            if n > 0:
                s = n - b
            else:
                s = 0
            model.Add(((country_data_list[n][2] == day_data_list[n][2]) and (country_data_list[n][2] == 1))).OnlyEnforceIf(shifts[(0, s)])
            model.Add(gnd_data_list[n][2] == 1).OnlyEnforceIf(shifts[(2, s)])

        for s in mod_shifts:
            if len(memory_keep) >= 1 and s == 0:
                num_pics = int(photos_keep[len(photos_keep) - 1])
                print(num_pics)
                memory = memory_keep[len(memory_keep) - 1]
                num_processed = int(processed_keep[len(processed_keep) - 1])

                num_pics = num_pics + (shifts[(0, s)] * 100) - (shifts[(2, s)] * (int(100 * downlink_data_rate / image_mem)))
                memory = memory + (image_mem * (shifts[(0, s)])) + (process_im_mem * shifts[(1, s)]) - (2 * downlink_data_rate * (shifts[(2, s)]))
                num_processed = num_processed + (shifts[(1, s)] * 100) - (shifts[(2, s)] * (int(100 * downlink_data_rate / process_im_mem)))
            else:
                num_pics += (shifts[(0, s)] * 100) - (shifts[(2, s)] * (int(100 * downlink_data_rate / image_mem)))
                memory += (image_mem * (shifts[(0, s)])) + (process_im_mem * shifts[(1, s)]) - (2 * downlink_data_rate * (shifts[(2, s)]))
                num_processed += (shifts[(1, s)] * 100) - (shifts[(2, s)] * (int(100 * downlink_data_rate / process_im_mem)))

            model.Add(num_processed > (int(100 * downlink_data_rate / process_im_mem))).OnlyEnforceIf(shifts[(2, s)])
            model.Add(num_pics > 0).OnlyEnforceIf(shifts[(1, s)])
            totaL_to_process = (num_pics * int((image_mem / process_im_mem)))
            model.Add(num_processed <= totaL_to_process)
            model.Add(memory < onboard_mem)
            summary.append([num_pics, num_processed, memory])

        model.Maximize(sum(shifts[(2, s)] + shifts[(0, s)] for s in mod_shifts))

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

        status = solver.Solve(model)
        print(status)

        final_list = []

        for n in range(b, c):
            if n > 0 and n < c:
                s = n - b
            elif n == c:
                s = n - b
                time_interval = time_interval - 1
            else:
                s = 0
            check_single_action = 0
            for a in all_actions:

                print(a, n, b, s)
                # print('shifts',solver.Value(shifts[(a, s)]))
                if solver.Value(shifts[(a, s)]) == 1:
                    memory_total = solver.Value(summary[s][2])
                    pics_taken = solver.Value(summary[s][0]) / 100
                    processed_images = solver.Value(summary[s][1]) / 100
                    check_single_action = check_single_action + 1
                    if a == 2:
                        downloaded_instances += 1
                    if a == 0:
                        pics_count += 1
                    if a == 1:
                        processed_pics_count += 1
                    # print('Action', a, 'works shift', n, 'time start', country_data_list[n][0])

                    if any(e[3] == n for e in final_list):
                        z = [i for i, lst in enumerate(final_list) if n in lst][0]
                        print('Removing Action', a, 'works shift', n, 'time start', country_data_list[n][0], 'NO')
                        print('pop')
                        print('Adding Action', a, 'works shift', n, 'time start', country_data_list[n][0], 'YES')
                        q = final_list.pop(z)
                        # print('Action', a, 'works shift', n, 'time start', country_data_list[n][0])  # ,summary[s][0],summary[s][1])
                        final_list.append(
                            [country_data_list[n][0], country_data_list[n][0] + time_interval, a, n, memory_total, pics_taken, pics_count, processed_images, processed_pics_count,
                             processed_pics_count / (image_mem / process_im_mem),
                             downloaded_instances, downloaded_instances / (image_mem / downlink_data_rate), idle_time, 'YES'])
                    else:
                        print('Action', a, 'works shift', n, 'time start', country_data_list[n][0], 'YES')  # ,summary[s][0],summary[s][1])
                        final_list.append([country_data_list[n][0], country_data_list[n][0] + time_interval, a, n, memory_total, pics_taken, pics_count, processed_images, processed_pics_count,
                                           processed_pics_count / (image_mem / process_im_mem),
                                           downloaded_instances, downloaded_instances / (image_mem / downlink_data_rate), idle_time, 'YES'])

                elif any(e[3] == n for e in final_list):
                    l = 1

                else:
                    print('Action', a, 'works shift', n, 'time start', country_data_list[n][0], 'NO')
                    idle_time += 1
                    final_list.append([country_data_list[n][0], country_data_list[n][0] + time_interval, a, n, memory_total, pics_taken, pics_count, processed_images, processed_pics_count,
                                       processed_pics_count / (image_mem / process_im_mem),
                                       downloaded_instances, downloaded_instances / (image_mem / downlink_data_rate), idle_time, 'NO'])

            if check_single_action > 1:
                print('ERROR: more than one action per time step')
                    # combined_lists=final_list
                    # combined_lists.append([final_list1])
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

        memory_keep.append(memory_total)
        processed_keep.append(processed_images * 100)
        photos_keep.append(pics_taken * 100)
        # summary =[]
        print(memory_keep)
        print(processed_pics_count)
        i = c