from manual_memory_plot import manual_memory_plot
from Solver_plot import solver_plot
from gantt_plot import gantt_plot


day = 1
#open files
daily_schedule = '../../Results/Day ' + str(day) + '/daily_schedule' + str(day) + '.txt'
manual_memory = '../../Results/Day ' + str(day) + '/manual_memory_states' + str(day) + '.txt'
manual_memory_binary = '../../Results/Day ' + str(day) + '/binary_daily_schedule' + str(day) + '.txt'
solver_memory = '../../Results/Day ' + str(day) + '/Solver/Optimized_results' + str(day) + '.txt'

#save images/plots
manual_plot_image = '../../Results/Day ' + str(day) + '/graphs/manual_memory_plot' + str(day) + '.png'
solver_plot_image = '../../Results/Day ' + str(day) + '/graphs/optimal_memory_plot' + str(day) + '.png'
gantt_plott_image = '../../Results/Day ' + str(day) + '/graphs/gantt_plot' + str(day) + '.png'

manual_binary_data = manual_memory_plot(manual_memory,manual_memory_binary,manual_plot_image)
constraint_land_list = solver_plot(solver_memory,solver_plot_image)
gantt_plot(manual_binary_data,daily_schedule,constraint_land_list,gantt_plott_image)


