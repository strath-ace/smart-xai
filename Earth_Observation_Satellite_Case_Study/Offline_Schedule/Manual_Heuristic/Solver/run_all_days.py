import os
from CPModel_with_Hint import CPModel_data
from CPSolver import CP_solver

# functions imported
from Earth_Observation_Satellite_Case_Study.Offline_Schedule.Manual_Heuristic.Manually_created_schedule.Manual_heuristic import heuristic
from Earth_Observation_Satellite_Case_Study.Offline_Schedule.Manual_Heuristic.Manually_created_schedule.Heuristic_memory_calculation import Manual_heuristic_memory_calculation
from Earth_Observation_Satellite_Case_Study.Offline_Schedule.Manual_Heuristic.Manually_created_schedule.Manual_binary_data import manual_binary_data
from Earth_Observation_Satellite_Case_Study.Offline_Schedule.Manual_Heuristic.graph_plot_code.manual_memory_plot import manual_memory_plot
from Earth_Observation_Satellite_Case_Study.Offline_Schedule.Manual_Heuristic.graph_plot_code.Solver_plot import solver_plot
from Earth_Observation_Satellite_Case_Study.Offline_Schedule.Manual_Heuristic.graph_plot_code.gantt_plot import gantt_plot
from Earth_Observation_Satellite_Case_Study.Environment.environment_data_to_solver import environment_data

days = 8
n = 3
while n in range(1, days):
    # Manual Schedule generation function
    day = n
    month = 'Dec'
    year = 2020
    country = 'All'

    time_interval = 5
    interval = 3000
    # hardware limitations of satellites
    onboard_mem = 0.8 * 24 * 10 ** 5
    # memory required per image
    image_mem = 2688
    downlink_data_rate = -280 * time_interval
    # 5000Kbit/s to process images
    process_im_mem = 50 * time_interval
    Max_pictures = int(onboard_mem / image_mem)

    filename = '../../Results/Day '
    path = '../../../Environment/'

    # create a new folder 'Day #' and sub folders if the folder doesnt exist
    if os.path.isdir(filename + str(day)):
        print('true')
        print('File ' + filename + str(day) + ' exists')
        if os.path.isdir(filename + str(day) + 'graphs'):
            print('File ' + filename + str(day) + 'graphs exists')
        else:
            os.makedirs(filename + str(day) + 'graphs')

        if os.path.isdir(filename + str(day) + 'Solver'):
            print('File ' + filename + str(day) + 'Solver exists')
        else:
            os.makedirs(filename + str(day) + 'Solver')

    else:
        os.makedirs(filename + str(day))
        os.makedirs(filename + str(day) + 'graphs')
        os.makedirs(filename + str(day) + 'Solver')

    # open files
    daily_schedule = '../../Results/Day ' + str(day) + '/daily_schedule' + str(day) + '.txt'
    manual_memory = '../../Results/Day ' + str(day) + '/manual_memory_states' + str(day) + '.txt'
    manual_memory_binary = '../../Results/Day ' + str(day) + '/binary_daily_schedule' + str(day) + '.txt'
    solver_memory = '../../Results/Day ' + str(day) + '/Solver/Optimized_results' + str(day) + '.txt'

    # save images/plots
    manual_plot_image = '../../Results/Day ' + str(day) + '/graphs/manual_memory_plot' + str(day) + '.png'
    solver_plot_image = '../../Results/Day ' + str(day) + '/graphs/optimal_memory_plot' + str(day) + '.png'
    gantt_plot_image = '../../Results/Day ' + str(day) + '/graphs/gantt_plot' + str(day) + '.png'

    # functions called
    heuristic(filename, day, month, year, country, time_interval)
    Manual_heuristic_memory_calculation(filename, day, month, time_interval, onboard_mem, image_mem, downlink_data_rate, process_im_mem)
    manual_binary_data(filename, time_interval, day, month)

    # calling the model and solver
    country_data_list, gnd_data_list, day_data_list = environment_data(path, time_interval, day, month, year, country)
    mem_data_list = manual_binary_data(filename, time_interval, day, month)[0]

    i = 0
    horizon = len(country_data_list)

    while i in range(0, horizon):
        model, summary, shifts, b, c = CPModel_data(day, interval, onboard_mem, image_mem, downlink_data_rate, process_im_mem, filename, mem_data_list, country_data_list,
                                                    gnd_data_list, day_data_list, horizon)

        c = CP_solver(b, c, day, shifts, image_mem, downlink_data_rate, process_im_mem, filename, country_data_list, model, summary, time_interval, horizon)
        i = c

    # plot the graphs
    manual_binary_data = manual_memory_plot(day, manual_memory, manual_memory_binary, manual_plot_image)
    constraint_land_list = solver_plot(day, solver_memory, solver_plot_image, image_mem, process_im_mem, onboard_mem, Max_pictures)
    gantt_plot(day, manual_binary_data, daily_schedule, constraint_land_list, gantt_plot_image)
    n += 1
