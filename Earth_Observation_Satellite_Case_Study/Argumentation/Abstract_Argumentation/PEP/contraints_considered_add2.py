# PEP calculation 4

def action_1(image_mem, memory_before_action, onboard_mem):
    if memory_before_action + image_mem <= onboard_mem:
        memory_after_action1 = memory_before_action + image_mem

    else:
        memory_after_action1 = -1
    return memory_after_action1


def action_2(num_images, memory_before_action, process_im_mem):
    if num_images >= 1 :
        # replace action memory at that point in time
        memory_after_action2 = memory_before_action + process_im_mem
    else:  # if less than 1 image is in memory
        memory_after_action2 = -1

    return  memory_after_action2

def action_3(num_process, memory_before_action, downlink_data_rate):
    # can it down-link? processing needs to occur 5.6 or 6 times (in memory) before down-link can take place
    if num_process >= 6:
        # yes it can down-link
        memory_after_action3 = memory_before_action - downlink_data_rate
    else:
        memory_after_action3 = -1
    return memory_after_action3

def action_4 (memory_before_action):
    memory_after_action4 = memory_before_action
    return memory_after_action4



def attack_calculation(a2, addrx, mem, lines_cp_coord, lines_attack_coord):
    time_interval = 5
    # onboard memory is 80% of total memory
    onboard_mem = int(0.8 * 24 * 10 ** 5)
    #  memory required per image
    image_mem = 2688
    # downlink data rate
    downlink_data_rate = 280 * 2 * time_interval
    # 5000Kbit/s to process images
    process_im_mem = 50 * time_interval


    S = int(lines_attack_coord[addrx].split()[4])

    land = int(lines_attack_coord[addrx].split()[1])
    station = int(lines_attack_coord[addrx].split()[2])
    day = int(lines_attack_coord[addrx].split()[3])
    num_images = float(lines_cp_coord[addrx-1].split()[5])
    num_process = float(lines_cp_coord[addrx-1].split()[7])
    memory_before_action = mem
    memory_after_action = -1

    # The satellite is over land, station and in day (all actions can occur)
    if day == land == station and land == 1 and memory_before_action <= onboard_mem:
        if S == 0:
            if a2 =='1':
                memory_after_action = action_2(num_images, memory_before_action, process_im_mem)
            elif a2 == '2':
                memory_after_action = action_3(num_process, memory_before_action, downlink_data_rate)
            elif a2 == '-1':
                memory_after_action = action_4(memory_before_action)

        elif S == 1:
            if a2 == '0' :
                memory_after_action = action_1(image_mem, memory_before_action, onboard_mem)
            elif a2 == '2':
                memory_after_action = action_3(num_process, memory_before_action, downlink_data_rate)
            elif a2 == '-1':
                memory_after_action = action_4(memory_before_action)
        elif S == 2:
            if a2 == '0' :
                memory_after_action = action_1(image_mem, memory_before_action, onboard_mem)
            elif a2 =='1':
                memory_after_action = action_2( num_images, memory_before_action, process_im_mem)
            elif a2 == '-1':
                memory_after_action = action_4(memory_before_action)
        else:
            memory_after_action = -1

    #The satellite is over land, in day but not over station (can take images and can process images)
    elif day == land == 1 and station == 0 and memory_before_action <= onboard_mem:
        if S == 0:
            if a2 =='1':
                memory_after_action = action_2( num_images, memory_before_action, process_im_mem)
            elif a2 == '-1':
                memory_after_action = action_4(memory_before_action)
        elif S == 1:
            if a2 == '0' :
                memory_after_action = action_1(image_mem, memory_before_action, onboard_mem)
            elif a2 == '-1':
                memory_after_action = action_4(memory_before_action)
        else:
            memory_after_action = -1

    # Over land and station but not in sunlight (can downlink and process images)
    elif land == station == 1 and day == 0 and memory_before_action <= onboard_mem:
        if S == 1:
            if a2 == '2':
                memory_after_action = action_3(num_process, memory_before_action, downlink_data_rate)
            elif a2 == '-1':
                memory_after_action = action_4(memory_before_action)
        elif S == 2:
            if a2 =='1':
                memory_after_action = action_2(num_images, memory_before_action, process_im_mem)
            elif a2 == '-1':
                memory_after_action = action_4(memory_before_action)
        else:
            memory_after_action = -1

    # Over station but not in sunlight or over land (can downlink and process images)
    elif station == 1 and land == 0 and memory_before_action <= onboard_mem:
        if S == 1:
            if a2 == '2':
                memory_after_action = action_3(num_process, memory_before_action, downlink_data_rate)
            elif a2 == '-1':
                memory_after_action = action_4(memory_before_action)
        elif S == 2:
            if a2 =='1':
                memory_after_action = action_2( num_images, memory_before_action, process_im_mem)
            elif a2 == '-1':
                memory_after_action = action_4(memory_before_action)
        else:
            memory_after_action = -1

    else:
        memory_after_action = -1
    #print('mem action',memory_after_action)
    return memory_after_action