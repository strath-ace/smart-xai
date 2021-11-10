# This function is a test environment used for creating a manual schedule for the satellite for a selected day

# functions imported
from Manual_heuristic import heuristic
from Heuristic_memory_calculation import Manual_heuristic_memory_calculation
from Manual_binary_data import  manual_binary_data

day = 1
month = 'Dec'
year = 2020
country = 'All'
path = '../../Results/Day '
time_interval = 5

# hardware limitations of satellites
onboard_mem = 0.8 * 24 * 10 ** 5
# memory required per image
image_mem = 2688
downlink_data_rate = -280 * time_interval
# 5000Kbit/s to process images
process_im_mem = 50 * time_interval

# functions called
heuristic(path, day, month, year, country,time_interval)
Manual_heuristic_memory_calculation(path, day, month, time_interval, onboard_mem, image_mem, downlink_data_rate, process_im_mem)
manual_binary_data(path, time_interval, day, month)