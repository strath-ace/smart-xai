# This function is used for calculating the memory from the generated manual schedule over a given day

# Prevents memory usage from exceeding the onboard memory and counts the occurrences for each action
def action_determination(final_jobs, onboard_mem, tot_pic, image_mem, process_im_mem, tot_proc, count_pic, count_proc, tot_down, count_down, downlink_data_rate, final_total):
    if final_jobs == '1' and ((image_mem * tot_pic) + (process_im_mem * tot_proc)) < onboard_mem:

        pic_chosen = 1
        tot_pic += 1
        count_pic += 1
        Demands = image_mem * pic_chosen

    elif final_jobs == '2' and tot_proc < (tot_pic * image_mem / process_im_mem) and ((image_mem * tot_pic) + (process_im_mem * tot_proc)) < onboard_mem:
        tot_proc += 1
        count_proc += 1
        Demands = process_im_mem  # * time_interval

    elif final_jobs == '3':
        Demands = 0

    elif final_jobs == '4' and tot_proc > image_mem / process_im_mem:  # and  (tot_proc > (-downlink_data_rate/process_im_mem)):
        tot_down += 1
        count_down += 1
        tot_proc = tot_proc + (downlink_data_rate / process_im_mem)
        tot_pic = tot_pic + (downlink_data_rate / image_mem)
        Demands = 2 * downlink_data_rate
        # Demands = -(final_total[len(final_total)-1]-Demands)

    else:
        Demands = 0

    return Demands, tot_pic, tot_proc, tot_down, count_down, count_pic, count_proc


# calculates the memory based on whether or not its a first run
def Memory_calculation_support_1(first_run, h, final_start, final_jobs, tot_down, tasks_list, tot_pic, count_pic, image_mem, onboard_mem, process_im_mem, tot_proc, count_proc, count_down, downlink_data_rate,
                                 final_total):
    z = 0
    start = int(final_start / 1000) + h

    tasks = final_jobs
    if z < 1000:
        z += 1
        tot_down = tot_down
    else:
        tot_down = 0

    if first_run == 1:
        if '1' in tasks_list:
            Demands, tot_pic, tot_proc, tot_down, count_down, count_pic, count_proc = action_determination(final_jobs, onboard_mem, tot_pic, image_mem, process_im_mem, tot_proc, count_pic, count_proc, tot_down,
                                                                                                           count_down, downlink_data_rate, final_total)
        else:
            # checks if the job action is 1 and the images taken is less than the total number of images allowed, increment and count the number of images
            if final_jobs == '1' and (tot_pic <= onboard_mem / image_mem):
                tot_pic += 1
                count_pic += 1
                pic_chosen = 1
                Demands = image_mem * pic_chosen
            else:
                Demands = 0
    else:
        Demands, tot_pic, tot_proc, tot_down, count_down, count_pic, count_proc = action_determination(final_jobs, onboard_mem, tot_pic, image_mem, process_im_mem, tot_proc, count_pic, count_proc, tot_down, count_down,
                                                                                                       downlink_data_rate, final_total)

    return start, Demands, tasks, tot_pic, tot_proc, tot_down, count_down, count_pic, count_proc
