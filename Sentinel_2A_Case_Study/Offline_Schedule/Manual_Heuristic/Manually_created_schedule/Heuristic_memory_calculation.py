import pandas as pd
import datetime as dt
from Manual_file_recall import Manual_file_recall
from Memory_calculation_support_1 import Memory_calculation_support_1
from Memory_calculation_support_2 import Memory_calculation_support_2


def Manual_heuristic_memory_calculation(patha, day, month):
    file1 = open(patha + str(day) + '/manual_memory_states' + str(day) + '.txt', "w")
    file2 = open(patha + str(day) + '/manual_memory_states_seconds' + str(day) + '.txt', "w")
    time_interval = 5
    onboard_mem = 0.8 * 24 * 10 ** 5
    # memory required per image
    image_mem = 2688
    downlink_data_rate = -280 * time_interval
    # 5000Kbit/s to process images
    process_im_mem = 50 * time_interval
    node_count_coord, lines_coord, tot_pic, tot_proc, tot_down, tot_idle, count_pic, count_proc, count_down, final_total = Manual_file_recall(patha, day, image_mem, downlink_data_rate, process_im_mem)

    Demands_mem = []
    total_pics = []
    print_list = []
    print_list2 = []
    tasks_list = []

    for task in range(0, node_count_coord):

        line_details = lines_coord[task].split()
        final_end = int(line_details[2])
        final_start = int(line_details[1])
        final_jobs = line_details[4]

        if day == 1 and month == 'Dec':
            first_run = 1
            h = 0
        else:
            first_run = 0
            h = 1

        while h <= (int(final_end / 1000) - int(final_start / 1000)) and (int(final_end / 1000) - int(final_start / 1000)) > time_interval:
            # for i in range(int(final_start[task]/1000),int(final_end[task]/1000)):
            start,Demands,tasks,tot_pic,tot_proc,tot_down, count_down,count_pic,count_proc = Memory_calculation_support_1(first_run, h, final_start, final_jobs, tot_down, tasks_list, tot_pic, count_pic, image_mem, onboard_mem,
                                                                                                          Demands_mem, process_im_mem, tot_proc, count_proc, count_down, downlink_data_rate, final_total)

            total, Actives, tot_pic, count_pic, tot_idle = Memory_calculation_support_2(Demands, final_total, h, tot_idle, onboard_mem, final_jobs, tot_proc, count_proc, count_pic, tot_pic, total_pics)

            end = start + time_interval

            final_total.append(total)
            tasks_list.append(tasks)
            Demands_mem.append(Demands)
            # total pics left in memory
            total_pics.append(tot_pic)

            # print([str(dt.timedelta(seconds=start)), end, tasks, Demands_mem, h, final_total, Actives, total_pics, tot_proc / (image_mem / process_im_mem),
            #        tot_down / (image_mem / -downlink_data_rate), tot_idle, count_pic, count_proc / (image_mem / process_im_mem), count_down / (image_mem / -downlink_data_rate)])

            print_list.append([str(dt.timedelta(seconds=start)), str(dt.timedelta(seconds=end)), tasks, Demands, h, total, Actives, tot_pic,
                               tot_proc / (image_mem / process_im_mem),
                               tot_down / (image_mem / -downlink_data_rate), tot_idle, count_pic, count_proc / (image_mem / process_im_mem), count_down / (image_mem / -downlink_data_rate)])

            print_list2.append([start, end, tasks, Demands, h, total, Actives, tot_pic, tot_proc / (image_mem / process_im_mem),
                                tot_down / (image_mem / -downlink_data_rate), tot_idle, count_pic, count_proc / (image_mem / process_im_mem), count_down / (image_mem / -downlink_data_rate)])

            h += time_interval

    print(print_list)
    df1 = pd.DataFrame(print_list)
    file1.writelines(df1.to_string(header=False, index=False))
    file1.close()

    df2 = pd.DataFrame(print_list2)
    file2.writelines(df2.to_string(header=False, index=False))
    file2.close()
