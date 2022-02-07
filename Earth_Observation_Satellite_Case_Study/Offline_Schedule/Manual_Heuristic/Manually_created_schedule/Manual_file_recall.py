# Function used to check if files for previous day exist and forward the last generated results from the previous day to the current day

def Manual_file_recall(patha, day, image_mem, downlink_data_rate, process_im_mem):
    # all values initialised
    tot_pic = 0
    tot_proc = 0
    tot_down = 0
    tot_idle = 0
    node_count_coord = 0
    # count the number of instances process has occurred
    count_proc = 0
    count_pic = 0
    count_down = 0
    final_total = []
    lines_coord = []

    if day == 1:
        path = patha + str(day) + '/Manual_Results' + str(day) + '.txt'
        f_coord = open(path, "r")
        line_count_coord = 0
        for line in f_coord:
            if line != "\n":
                line_count_coord += 1
        f_coord.close()

        f_coord = open(path, "r")
        node_count_coord = line_count_coord
        content_coord = f_coord.read()
        lines_coord = content_coord.split('\n')

    elif day > 1:
        # file for current day
        filename = patha + str(day) + '/Manual_Results' + str(day) + '.txt'
        # call file for previous day to extract last read values
        filename2 = patha + str(day - 1) + '/manual_memory_states' + str(day - 1) + '.txt'

        # read filename data for current day
        f_coord = open(filename, "r")
        line_count_coord = 0
        for line in f_coord:
            if line != "\n":
                line_count_coord += 1
        f_coord.close()

        f_coord = open(filename, "r")
        node_count_coord = line_count_coord
        content_coord = f_coord.read()
        lines_coord = content_coord.split('\n')

        # read filename data for previous day
        f_coord1 = open(filename2, "r")
        line_count_coord1 = 0
        for line in f_coord1:
            if line != "\n":
                line_count_coord1 += 1
        f_coord1.close()

        f_coord1 = open(filename2, "r")
        node_count_coord1 = line_count_coord1
        content_coord1 = f_coord1.read()
        lines_coord1 = content_coord1.split('\n')
        lines_data1 = lines_coord1[node_count_coord1 - 1].split()
        print(lines_data1)

        # initialize values for current day from last data for previous day
        initial_total = int(lines_data1[5])
        final_total = [initial_total]
        # left in memory
        tot_pic = float(lines_data1[7])
        tot_proc = float(lines_data1[8]) * (image_mem / process_im_mem)
        tot_down = (-image_mem / downlink_data_rate)
        tot_idle = int(lines_data1[10])
        # count the number of instances process has occurred
        count_pic = int(lines_data1[11])
        count_proc = float(lines_data1[12]) * (image_mem / process_im_mem)
        count_down = float(lines_data1[13]) * (-image_mem / downlink_data_rate)

    else:
        print('ERROR')

    return node_count_coord, lines_coord, tot_pic, tot_proc, tot_down, tot_idle, count_pic, count_proc, count_down, final_total
