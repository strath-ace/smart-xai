from Manual_heuristic import heuristic
from Heuristic_memory_calculation import Manual_heuristic_memory_calculation
from Manual_binary_data import  manual_binary_data

day = 2
month = 'Dec'
year = 2020
country = 'All'
path = '../../Results/Day '
time_interval = 5
heuristic(path, day, month, year, country)
Manual_heuristic_memory_calculation(path,day,month)
manual_binary_data(path, time_interval, day, month)