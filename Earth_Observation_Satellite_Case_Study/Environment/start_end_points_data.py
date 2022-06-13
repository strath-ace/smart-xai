# ------------------Copyright (C) 2022 University of Strathclyde and Author ---------------------------------
# --------------------------------- Author: Cheyenne Powell -------------------------------------------------
# ------------------------- e-mail: cheyenne.powell@strath.ac.uk --------------------------------------------

# This file is used for determining the start and end times for each day.
# ===========================================================================================================

import datetime as dt
# Import function to determine start and end time of the day
def time_select(day,month):
    # The first day is 1st of December that starts at 11:00am - YY MM DD is removed and only day is factored.
    if day == 1 and month =='Dec':
        start_second_interval = int(
            ((dt.datetime.strptime(str('11:00:00.10'), '%H:%M:%S.%f') - dt.datetime(1900, 1, 1)).total_seconds()))
    # Ensures the date is never the 1st of december - can be rewritten as 'elif day >=1:' for time to start at 00:00.
    elif day ==1 and month !='Dec':
        start_second_interval = int(
            ((dt.datetime.strptime(str('00:00:01.10'), '%H:%M:%S.%f') - dt.datetime(1900, 1, 1)).total_seconds()))
    elif day > 1:
        start_second_interval = int(
            ((dt.datetime.strptime(str('00:00:01.10'), '%H:%M:%S.%f') - dt.datetime(1900, 1, 1)).total_seconds()))
    else:
        print('Please Enter a valid day')

    # End time for every day is 23:59:59.
    end_second_interval = int(
        ((dt.datetime.strptime(str('23:59:59.59'), '%H:%M:%S.%f') - dt.datetime(1900, 1, 1)).total_seconds()))

    return start_second_interval, end_second_interval
