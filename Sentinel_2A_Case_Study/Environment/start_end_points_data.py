import datetime as dt
#import function to determine start and end time of the day
def time_select(day,month):
    #the first day is 1st of December that starts at 11:00am - YY MM DD is removed and only day is factored
    if day == 1 and month =='Dec':
        start_second_interval = int(
            ((dt.datetime.strptime(str('11:00:00.10'), '%H:%M:%S.%f') - dt.datetime(1900, 1, 1)).total_seconds()))
    #ensures the date is never the 1st of december - can be rewritten as 'elif day >=1:' for time to start at 00:00
    elif day ==1 and month !='Dec':
        start_second_interval = int(
            ((dt.datetime.strptime(str('00:00:01.10'), '%H:%M:%S.%f') - dt.datetime(1900, 1, 1)).total_seconds()))
    elif day > 1:
        start_second_interval = int(
            ((dt.datetime.strptime(str('00:00:01.10'), '%H:%M:%S.%f') - dt.datetime(1900, 1, 1)).total_seconds()))
    else:
        print('Please Enter a valid day')
    #end time for every day is 23:59:59
    end_second_interval = int(
        ((dt.datetime.strptime(str('23:59:59.59'), '%H:%M:%S.%f') - dt.datetime(1900, 1, 1)).total_seconds()))

    return start_second_interval, end_second_interval
