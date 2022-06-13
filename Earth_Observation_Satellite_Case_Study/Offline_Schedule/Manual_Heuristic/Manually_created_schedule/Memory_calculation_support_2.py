# ------------------Copyright (C) 2022 University of Strathclyde and Author ---------------------------------
# --------------------------------- Author: Cheyenne Powell -------------------------------------------------
# ------------------------- e-mail: cheyenne.powell@strath.ac.uk --------------------------------------------

# This function is used for calculating the total memory from the generated manual schedule over a given day \
# and determines whether the activity is to occur as well as calculate the total number of instances for each activity

# ===========================================================================================================

def Memory_calculation_support_2(Demands, final_total, h, tot_idle, onboard_mem, final_jobs, tot_proc, count_proc,
                                 count_pic, tot_pic, total_pics):
    total = Demands
    actives = ''
    if h == 0 and len(final_total) == 0 and total == 0:
        total = Demands
        actives = False

    elif h == 0 and len(final_total) == 0 and total > 0:
        total = Demands
        actives = True

    elif h == 0 and len(final_total) == 0 and total < 0:
        total = 0
        actives = False

    elif h == 0 and final_total[len(final_total) - 1] > 0 and Demands != 0:
        total = final_total[len(final_total) - 1] + Demands

        if 0 < total <= onboard_mem:
            total = Demands + final_total[len(final_total) - 1]
            actives = True
        else:
            total = final_total[len(final_total) - 1]
            actives = False

    elif h > 0 and final_total[len(final_total) - 1] > 0 and Demands != 0:
        total = final_total[len(final_total) - 1] + Demands

        if 0 < total <= onboard_mem:
            total = Demands + final_total[len(final_total) - 1]
            actives = True
        else:
            total = final_total[len(final_total) - 1]
            actives = False

    elif (h == 0 or h > 0) and final_total[len(final_total) - 1] == 0 and Demands != 0:
        total = final_total[len(final_total) - 1] + Demands

        if 0 < total <= onboard_mem:
            total = Demands + final_total[len(final_total) - 1]
            actives = True
        else:
            total = final_total[len(final_total) - 1]
            actives = False

    elif Demands == 0:
        total = Demands + final_total[len(final_total) - 1]
        actives = False

    if final_jobs == '1' and actives is False and tot_pic > 0:
        tot_pic -= 1
        count_pic -= 1

    if actives is False:
        tot_idle += 1

    return total, actives, tot_pic, count_pic, tot_idle
