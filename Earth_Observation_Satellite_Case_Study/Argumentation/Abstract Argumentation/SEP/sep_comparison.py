# File number 1 to extract data from solver schedule and create options where attacks can occur
import pandas as pd
from Earth_Observation_Satellite_Case_Study.Environment.environment_data_to_solver import environment_data

# action 1 function called if images can be taken
def action_1(image_mem, memory_before_action, final_day_memory, memory_of_old_action, onboard_mem):
    if memory_before_action + image_mem <= onboard_mem:
        extracted_action1 = 0
        memory_after_action1 = memory_before_action + image_mem
        # final memory recalculated with initial action replaced with new action
        final_day_memory1 = final_day_memory - memory_of_old_action + image_mem
        if final_day_memory1 < onboard_mem:
            final_day_memory1_message = 'Memory_within_limit:_' + str(final_day_memory1)
        else:
            final_day_memory1_message = 'Memory_exceeded_limit:_' + str(final_day_memory1)
    else:
        extracted_action1 = '00'
        memory_after_action1 = '00'
        final_day_memory1 = final_day_memory
        final_day_memory1_message = 'Use_original_action:_' + str(final_day_memory)
    return extracted_action1, memory_after_action1, final_day_memory1, final_day_memory1_message

# action 2 function called if image processing can occur
def action_2(num_images, memory_before_action, process_im_mem, final_day_memory, memory_of_old_action, onboard_mem):
    if num_images >= 1:
        # yes it can process
        extracted_action2 = 1
        # replace action memory at that point in time
        memory_after_action2 = memory_before_action + process_im_mem
        # final memory recalculated with revised action
        final_day_memory2 = final_day_memory - memory_of_old_action + process_im_mem
        if final_day_memory2 < onboard_mem:
            final_day_memory2_message = 'Memory_within_limit:_' + str(final_day_memory2)
        else:
            final_day_memory2_message = 'Memory_exceeded_limit:_' + str(final_day_memory2)
    else:  # if less than 1 image is in memory
        extracted_action2 = '00'
        memory_after_action2 = '00'
        final_day_memory2 = final_day_memory
        final_day_memory2_message = 'Use_original_action:_' + str(final_day_memory)
    return extracted_action2, memory_after_action2, final_day_memory2, final_day_memory2_message

# action 3 function called if images can be down-linked
def action_3(num_process, memory_before_action, downlink_data_rate, final_day_memory, memory_of_old_action, onboard_mem):
    # can it down-link? processing needs to occur 5.6 or 6 times (in memory) before down-link can take place
    if num_process >= 6:
        # yes it can down-link
        extracted_action3 = 2
        memory_after_action3 = memory_before_action - downlink_data_rate
        final_day_memory3 = final_day_memory - memory_of_old_action - downlink_data_rate
        if onboard_mem > final_day_memory3 > downlink_data_rate:
            final_day_memory3_message = 'Memory_within_limit:_' + str(final_day_memory3)
        else:
            final_day_memory3_message = 'Memory_exceeded_limit:_' + str(final_day_memory3)
    else:
        extracted_action3 = '00'
        memory_after_action3 = '00'
        final_day_memory3 = final_day_memory
        final_day_memory3_message = 'Use_original_action:_' + str(final_day_memory)
    return extracted_action3, memory_after_action3, final_day_memory3, final_day_memory3_message

# initial function to determine where attacks can occur throughout the schedule for selected day
def initial_attack_calculation():
    # Day 3 selected
    day = 3
    month = 'Dec'
    year = 2020
    country = 'All'
    time_interval = 5
    # interval = 3000
    # onboard memory is 80% of total memory
    onboard_mem = int(0.8 * 24 * 10 ** 5)
    #  memory required per image
    image_mem = 2688
    # downlink data rate
    downlink_data_rate = 280 * 2 * time_interval
    # 5000Kbit/s to process images
    process_im_mem = 50 * time_interval

    filename = 'SEP_Results/Day/Day' + str(day) + '.txt'

    absolute_path = 'C:/Users/User/Documents/GitHub/smart-xai'
    # loading the satellites position based on date
    path = absolute_path + '/Earth_Observation_Satellite_Case_Study/Environment/'
    country_data_list, gnd_data_list, day_data_list = environment_data(path, time_interval, day, month, year, country)
    horizon = min(len(country_data_list), len(gnd_data_list), len(day_data_list))
    # print(country_data_list, gnd_data_list, day_data_list)
    print(len(country_data_list))

    # loading the solvers results
    solver_path = 'SEP_Results/Day/Optimized_results' + str(day) + '.txt'
    solver_coord = open(solver_path, "r")
    count_coord = 0
    # for loop to count the number of lines in file
    for line in solver_coord:
        if line != "\n":
            count_coord += 1
    solver_coord.close()
    print(count_coord)

    # load data line by line
    solver_coord = open(solver_path, "r")
    content_cp_coord = solver_coord.read()
    lines_cp_coord = content_cp_coord.split('\n')
    # print(lines_cp_coord)

    SEP_data = [['time', 'land_access', 'station_access', 'day_access', 'extracted_action', 'memory_after_action', 'final_memory', 'action1', 'memory_after_action1', 'final_day_memory1', 'final_day_memory1_message',
                 'action2', 'memory_after_action2', 'final_day_memory2', 'final_day_memory2_message', 'action3', 'memory_after_action3', 'final_day_memory3', 'final_day_memory3_message']]

    horizon = horizon - 1

    for n in range(1, horizon):
        solver_details = lines_cp_coord[n].split()
        # check if action is executed
        if solver_details[15] == 'YES':
            extracted_action = int(solver_details[2])
        else:
            extracted_action = -1

        # loading original data from results
        memory_before_action = int(lines_cp_coord[n - 1].split()[4])
        memory_after_action = int(solver_details[4])
        final_day_memory = int(lines_cp_coord[horizon].split()[4])
        land_access = int(country_data_list[n][2])
        station_access = int(gnd_data_list[n][2])
        day_access = int(day_data_list[n][2])
        num_images = float(solver_details[5])
        num_process = float(solver_details[7])


        # all actions can take place
        if day_access == land_access == station_access and land_access == 1 and memory_after_action <= onboard_mem:
            # check if images taken is in schedule
            if extracted_action == 0:
                # original action always has a 00 , extracted_action1 represents image taken
                extracted_action1 = 0
                memory_after_action1 = memory_after_action
                final_day_memory1 = final_day_memory
                final_day_memory1_message = 'original_action:_' + str(final_day_memory)

                # check to see if it can process
                # can it process? check if there are more than 1 images taken to process and check if memory is exceeded with new action
                extracted_action2, memory_after_action2, final_day_memory2, final_day_memory2_message = action_2(num_images, memory_before_action, process_im_mem, final_day_memory, image_mem, onboard_mem)

                # check to see if it can down-link
                # can it down-link? processing needs to occur 5.6 or 6 times (in memory) before down-link can take place
                extracted_action3, memory_after_action3, final_day_memory3, final_day_memory3_message = action_3(num_process, memory_before_action, downlink_data_rate, final_day_memory, image_mem, onboard_mem)


            # if the action process is to take place
            elif extracted_action == 1:
                extracted_action2 = 1
                memory_after_action2 = memory_after_action
                final_day_memory2 = final_day_memory
                final_day_memory2_message = 'original_action:_' + str(final_day_memory)

                # check to see if images can take place
                extracted_action1, memory_after_action1, final_day_memory1, final_day_memory1_message = action_1(image_mem, memory_before_action, final_day_memory, process_im_mem, onboard_mem)

                # can it down-link? processing needs to occur 5.6 or 6 times (in memory) before down-link can take place
                extracted_action3, memory_after_action3, final_day_memory3, final_day_memory3_message = action_3(num_process, memory_before_action, downlink_data_rate, final_day_memory, process_im_mem, onboard_mem)

            # check if it's scheduled to down-link
            elif extracted_action == 2:
                extracted_action3 = 2
                memory_after_action3 = memory_after_action
                final_day_memory3 = final_day_memory
                final_day_memory3_message = 'original_action:_' + str(final_day_memory)

                # check to see if images can take place
                extracted_action1, memory_after_action1, final_day_memory1, final_day_memory1_message = action_1(image_mem, memory_before_action, final_day_memory, downlink_data_rate, onboard_mem)

                # check to see if it can process
                # can it process? check if there are more than 1 images taken to process and check if memory is exceeded with new action
                extracted_action2, memory_after_action2, final_day_memory2, final_day_memory2_message = action_2(num_images, memory_before_action, process_im_mem, final_day_memory, downlink_data_rate, onboard_mem)

            else:  # if action is idle

                # check to see if images can take place
                extracted_action1, memory_after_action1, final_day_memory1, final_day_memory1_message = action_1(image_mem, memory_before_action, final_day_memory, 0, onboard_mem)

                # check to see if it can process
                # can it process? check if there are more than 1 images taken to process and check if memory is exceeded with new action
                extracted_action2, memory_after_action2, final_day_memory2, final_day_memory2_message = action_2(num_images, memory_before_action, process_im_mem, final_day_memory, 0, onboard_mem)

                # can it down-link? processing needs to occur 5.6 or 6 times (in memory) before down-link can take place
                extracted_action3, memory_after_action3, final_day_memory3, final_day_memory3_message = action_3(num_process, memory_before_action, downlink_data_rate, final_day_memory, 0, onboard_mem)

            # SEP_data.append([solver_details[0], land_access, station_access, day_access, extracted_action, memory_after_action, final_day_memory, extracted_action1, memory_after_action1, final_day_memory1,
            #                      final_day_memory1_message, extracted_action2, memory_after_action2, final_day_memory2, final_day_memory2_message, extracted_action3, memory_after_action3, final_day_memory3,
            #                      final_day_memory3_message])

        # can only take images or process
        elif day_access == land_access == 1 and station_access == 0 and memory_after_action <= onboard_mem:
            extracted_action3 = '00'
            memory_after_action3 = '00'
            final_day_memory3 = final_day_memory
            final_day_memory3_message = 'Use_original_action:_' + str(final_day_memory)

            # if it's scheduled to take images
            if extracted_action == 0:
                # original action always has a 00 , extracted_action1 represents image taken
                extracted_action1 = 0
                memory_after_action1 = memory_after_action
                final_day_memory1 = final_day_memory
                final_day_memory1_message = 'original_action:_' + str(final_day_memory)
                # check to see if it can process
                # can it process? check if there are more than 1 images taken to process and check if memory is exceeded with new action
                extracted_action2, memory_after_action2, final_day_memory2, final_day_memory2_message = action_2(num_images, memory_before_action, process_im_mem, final_day_memory, image_mem, onboard_mem)


            # if the action is process
            elif extracted_action == 1:
                extracted_action2 = 1
                memory_after_action2 = memory_after_action
                final_day_memory2 = final_day_memory
                final_day_memory2_message = 'original_action:_' + str(final_day_memory)

                # check to see if images can take place
                extracted_action1, memory_after_action1, final_day_memory1, final_day_memory1_message = action_1(image_mem, memory_before_action, final_day_memory, process_im_mem, onboard_mem)


            # if the action is idle
            else:
                # can images be taken
                extracted_action1, memory_after_action1, final_day_memory1, final_day_memory1_message = action_1(image_mem, memory_before_action, final_day_memory, 0, onboard_mem)

                # check to see if it can process
                extracted_action2, memory_after_action2, final_day_memory2, final_day_memory2_message = action_2(num_images, memory_before_action, process_im_mem, final_day_memory, 0, onboard_mem)

            # SEP_data.append([solver_details[0], land_access, station_access, day_access, extracted_action, memory_after_action, final_day_memory, extracted_action1, memory_after_action1, final_day_memory1,
            #                      final_day_memory1_message, extracted_action2, memory_after_action2, final_day_memory2, final_day_memory2_message, extracted_action3, memory_after_action3, final_day_memory3,
            #                      final_day_memory3_message])

        # can only down-link or process
        elif land_access == station_access == 1 and day_access == 0 and memory_after_action <= onboard_mem:

            # let action a1 be '00' since images cant be taken
            extracted_action1 = '00'
            memory_after_action1 = '00'
            final_day_memory1 = final_day_memory
            final_day_memory1_message = 'Use_original_action:_' + str(final_day_memory)

            # if process is selected
            if extracted_action == 1:
                extracted_action2 = 1
                memory_after_action2 = memory_after_action
                final_day_memory2 = final_day_memory
                final_day_memory2_message = 'original_action:_' + str(final_day_memory)

                # can it down-link? processing needs to occur 5.6 or 6 times (in memory) before down-link can take place
                extracted_action3, memory_after_action3, final_day_memory3, final_day_memory3_message = action_3(num_process, memory_before_action, downlink_data_rate, final_day_memory, process_im_mem, onboard_mem)

            # if downlinking is selected
            elif extracted_action == 2:

                extracted_action3 = 2
                memory_after_action3 = memory_after_action
                final_day_memory3 = final_day_memory
                final_day_memory3_message = 'original_action:_' + str(final_day_memory)

                # check to see if it can process
                extracted_action2, memory_after_action2, final_day_memory2, final_day_memory2_message = action_2(num_images, memory_before_action, process_im_mem, final_day_memory, -downlink_data_rate, onboard_mem)

            # if it's idle
            else:
                # check to see if it can process
                # can it process? check if there are more than 1 images taken to process and check if memory is exceeded with new action
                extracted_action2, memory_after_action2, final_day_memory2, final_day_memory2_message = action_2(num_images, memory_before_action, process_im_mem, final_day_memory, 0, onboard_mem)

                # can it down-link? processing needs to occur 5.6 or 6 times (in memory) before down-link can take place
                extracted_action3, memory_after_action3, final_day_memory3, final_day_memory3_message = action_3(num_process, memory_before_action, downlink_data_rate, final_day_memory, 0, onboard_mem)

            # SEP_data.append([solver_details[0], land_access, station_access, day_access, extracted_action, memory_after_action, final_day_memory, extracted_action1, memory_after_action1, final_day_memory1,
            #                  final_day_memory1_message, extracted_action2, memory_after_action2, final_day_memory2, final_day_memory2_message, extracted_action3, memory_after_action3, final_day_memory3,
            #                  final_day_memory3_message])

        # only down-link or process
        elif station_access == 1 and land_access == 0 and memory_after_action <= onboard_mem:
            extracted_action1 = '00'
            memory_after_action1 = '00'
            final_day_memory1 = final_day_memory
            final_day_memory1_message = 'use_original_action:_' + str(final_day_memory)

            # if process is selected
            if extracted_action == 1:
                extracted_action2 = 1
                memory_after_action2 = memory_after_action
                final_day_memory2 = final_day_memory
                final_day_memory2_message = 'original_action:_' + str(final_day_memory)

                # can it down-link? processing needs to occur 5.6 or 6 times (in memory) before down-link can take place
                extracted_action3, memory_after_action3, final_day_memory3, final_day_memory3_message = action_3(num_process, memory_before_action, downlink_data_rate, final_day_memory, process_im_mem, onboard_mem)


            # if downlinking is selected
            elif extracted_action == 2:

                extracted_action3 = 2
                memory_after_action3 = memory_after_action
                final_day_memory3 = final_day_memory
                final_day_memory3_message = 'original_action:_' + str(final_day_memory)

                # check to see if it can process
                extracted_action2, memory_after_action2, final_day_memory2, final_day_memory2_message = action_2(num_images, memory_before_action, process_im_mem, final_day_memory, -downlink_data_rate, onboard_mem)


            # if it's idle
            else:
                # check to see if it can process
                # can it process? check if there are more than 1 images taken to process and check if memory is exceeded with new action
                extracted_action2, memory_after_action2, final_day_memory2, final_day_memory2_message = action_2(num_images, memory_before_action, process_im_mem, final_day_memory, 0, onboard_mem)

                # can it down-link? processing needs to occur 5.6 or 6 times (in memory) before down-link can take place
                extracted_action3, memory_after_action3, final_day_memory3, final_day_memory3_message = action_3(num_process, memory_before_action, downlink_data_rate, final_day_memory, 0, onboard_mem)

            # SEP_data.append([solver_details[0], land_access, station_access, day_access, extracted_action, memory_after_action, final_day_memory, extracted_action1, memory_after_action1, final_day_memory1,
            #                  final_day_memory1_message, extracted_action2, memory_after_action2, final_day_memory2, final_day_memory2_message, extracted_action3, memory_after_action3, final_day_memory3,
            #                  final_day_memory3_message])

        # for any other condition - only process possible
        else:

            extracted_action1 = '00'
            memory_after_action1 = '00'
            final_day_memory1 = final_day_memory
            final_day_memory1_message = 'Use_original_action:_' + str(final_day_memory)

            extracted_action3 = '00'
            memory_after_action3 = '00'
            final_day_memory3 = final_day_memory
            final_day_memory3_message = 'Use_original_action:_' + str(final_day_memory)
            # check to see if it can process
            # can it process? check if there are more than 1 images taken to process and check if memory is exceeded with new action
            extracted_action2, memory_after_action2, final_day_memory2, final_day_memory2_message = action_2(num_images, memory_before_action, process_im_mem, final_day_memory, 0, onboard_mem)

        SEP_data.append([solver_details[0], land_access, station_access, day_access, extracted_action, memory_after_action, final_day_memory, extracted_action1, memory_after_action1, final_day_memory1,
                         final_day_memory1_message, extracted_action2, memory_after_action2, final_day_memory2, final_day_memory2_message, extracted_action3, memory_after_action3, final_day_memory3,
                         final_day_memory3_message])

    file1 = open(filename, 'w')
    df = pd.DataFrame(SEP_data)
    file1.writelines(df.to_string(header=False, index=False))
    file1.close()


initial_attack_calculation()
