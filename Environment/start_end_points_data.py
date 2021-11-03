import datetime as dt

def time_select(day,month):
    if day == 1 and month =='Dec':
        start_second_interval = int(
            ((dt.datetime.strptime(str('11:00:00.10'), '%H:%M:%S.%f') - dt.datetime(1900, 1, 1)).total_seconds()))
    elif day ==1 and month !='Dec':
        start_second_interval = int(
            ((dt.datetime.strptime(str('00:00:01.10'), '%H:%M:%S.%f') - dt.datetime(1900, 1, 1)).total_seconds()))
    elif day > 1:
        start_second_interval = int(
            ((dt.datetime.strptime(str('00:00:01.10'), '%H:%M:%S.%f') - dt.datetime(1900, 1, 1)).total_seconds()))
    else:
        print('Please Enter a valid day')
    end_second_interval = int(
        ((dt.datetime.strptime(str('23:59:59.59'), '%H:%M:%S.%f') - dt.datetime(1900, 1, 1)).total_seconds()))

    return start_second_interval, end_second_interval
