from CPModel_with_Hint import CPModel_data
from CPSolver import CP_solver
from Sentinel_2A_Case_Study.Environment.environment_data_to_solver import environment_data
from Sentinel_2A_Case_Study.Offline_Schedule.Manual_Heuristic.Manually_created_schedule.Manual_binary_data import manual_data_retrieved

day = 1
month = 'Dec'
year = 2020
country = 'All'
time_interval = 5
interval = 3000
# onboard memory is 80% of total memory
onboard_mem = int(0.8 * 24 * 10 ** 5)
#  memory required per image
image_mem = 2688
# downlink data rate
downlink_data_rate = 280 * time_interval
# 5000Kbit/s to process images
process_im_mem = 50 * time_interval


filename = '../../Results/Day '
path = '../../../Environment/'
path1 = '../../Results/Day ' + str(day)

country_data_list, gnd_data_list, day_data_list = environment_data(path,time_interval, day, month, year, country)
mem_data_list = manual_data_retrieved(path1, time_interval, day, month)[0]

i = 0
horizon = len(country_data_list)

while i in range(0, horizon):
    model, summary, shifts, b,c = CPModel_data(day, interval, onboard_mem, image_mem, downlink_data_rate, process_im_mem, filename, mem_data_list, country_data_list,
                                             gnd_data_list, day_data_list, horizon)

    c = CP_solver(b, c, day, shifts, image_mem, downlink_data_rate, process_im_mem, filename, country_data_list, model, summary, time_interval)

    i = c


