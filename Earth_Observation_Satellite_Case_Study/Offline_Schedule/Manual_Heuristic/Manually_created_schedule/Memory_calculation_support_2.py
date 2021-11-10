# This function is used for calculating the total memory from the generated manual schedule over a given day and determines whether or not
# the activity is to occur as well as calculate the total number of instances for each activity

def Memory_calculation_support_2(Demands, final_total, h, tot_idle, onboard_mem, final_jobs, tot_proc, count_proc, count_pic, tot_pic, total_pics):
    total = Demands
    Actives = ''
    if h == 0 and len(final_total) == 0 and total == 0:
        total = Demands
        Actives = False

    elif h == 0 and len(final_total) == 0 and total > 0:
        total = Demands
        Actives = True

    elif h == 0 and len(final_total) == 0 and total < 0:
        total = 0
        Actives = False

    elif h == 0 and final_total[h - 1] > 0 and Demands != 0:
        total = final_total[h - 1] + Demands

        if 0 < total <= onboard_mem:
            total = Demands + final_total[h - 1]
            Actives = True
        else:
            total = final_total[h - 1]
            Actives = False

    elif h > 0 and final_total[len(final_total) - 1] > 0 and Demands != 0:
        total = final_total[len(final_total) - 1] + Demands

        if 0 < total <= onboard_mem:
            total = Demands + final_total[len(final_total) - 1]
            Actives = True
        else:
            total = final_total[len(final_total) - 1]
            Actives = False

    elif (h == 0 or h > 0) and final_total[len(final_total) - 1] == 0 and Demands != 0:
        total = final_total[len(final_total) - 1] + Demands

        if 0 < total <= onboard_mem:
            total = Demands + final_total[len(final_total) - 1]
            Actives = True
        else:
            total = final_total[len(final_total) - 1]
            Actives = False

    elif Demands == 0:
        total = Demands + final_total[len(final_total) - 1]
        Actives = False

    if final_jobs == '2' and Actives is False and tot_proc > 1:
        tot_proc -= 1
        count_proc -= 1

    if final_jobs == '1' and Actives is False and tot_pic > total_pics[len(total_pics) - 1]:
        tot_pic -= 1
        count_pic -= 1

    if Actives is False:
        tot_idle += 1

    return total, Actives, tot_pic, count_pic, tot_idle
