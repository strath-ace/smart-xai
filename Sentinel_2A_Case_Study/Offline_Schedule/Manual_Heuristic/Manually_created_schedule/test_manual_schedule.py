from Manual_Heuristic import heuristic
from Memory_calculation import Heuristic_memory_calculation
from Binary_day import  manual_data_retrieved

day = 1
month = 'Dec'
year = 2020
country = 'All'
path = '../../Results/Day ' + str(day)
time_interval = 5
heuristic(path, day, month, year, country)
Heuristic_memory_calculation(path,day)
manual_data_retrieved(path, time_interval, day, month)