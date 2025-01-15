# ------------------Copyright (C) 2023 University of Strathclyde and Author ---------------------------------
# --------------------------------- Author: Cheyenne Powell -------------------------------------------------
# ------------------------- e-mail: cheyenne.powell@strath.ac.uk --------------------------------------------

# creates a txt file and spreadsheet with the combined schedule and environmental conditions to provide to OpenAI
# enabling it to analyze the data and conditions
# ===========================================================================================================


import os
import sys
import pandas as pd

sys.path.append('../../')

from Environment.environment_data_to_solver import environment_data
from Map_image_coord import sat_coordinates
def main():

    day = 3
    filename = '../Results/Day' + str(day)



    # create a new folder 'Day #' and sub folders if the folder doesn't exist
    if os.path.isdir(filename):
        print('true')
        print('File ' + filename + ' exists')
    else:
        print('false')
        os.makedirs(filename)


    month = 'Dec'
    year = 2020
    country = 'All'
    time_interval = 5
    # onboard memory is 80% of total memory
    maximum_memory = int(0.8 * 24 * 10 ** 5)
    #  memory required per image
    image_mem = 2688
    # downlink data rate
    downlink_data_rate = 280 * 2 * time_interval
    # 5000Kbit/s to process images
    process_im_mem = 50 * time_interval


    # Loading the environmental conditions..
    path = '../../Environment/'
    # path = absolute_path + '/Earth_Observation_Satellite_Case_Study/Environment/'
    country_data_list, gnd_data_list, day_data_list = environment_data(path, time_interval, day, month, year, country)
    horizon = min(len(country_data_list), len(gnd_data_list), len(day_data_list))
    print(len(country_data_list))

    # Loading satellite's coordinates
    satellite_data = sat_coordinates(day, month, year, path)

    # match_coord = cross_ref(filename, initial_solver_memory_path, day, month, year)
    # print('match data', match_coord)



    # Loading the solvers results.
    solver_path = '../../Offline_Schedule/Results_with max(pic,proc,down)/Day ' + str(
        day) + '/Solver/Optimized_results' + str(day) + '.txt'
    # solver_path = '../../../Offline_Schedule/Results_with max(pic,proc,down)/Day ' + str(
    #     day) + '/Solver/Optimized_results' + str(day) + '.txt'
    solver_coord = open(solver_path, "r")
    count_coord = 0

    # For loop to count the number of lines in file.
    for line in solver_coord:
        if line != "\n":
            count_coord += 1
    solver_coord.close()
    print(count_coord)

    # Load data line by line.
    solver_coord = open(solver_path, "r")
    content_cp_coord = solver_coord.read()
    lines_cp_coord = content_cp_coord.split('\n')



    # Headings for data file.
    data = [['start_time', 'end_time', 'latitude', 'longitude', 'land_access', 'station_access', 'day_access', 'extracted_action', 'n', 'memory_used', 'maximum_memory',
                 'pics_in_memory', 'total_pics_count', 'processed_images_in_memory', 'total_processed_instances','total_processed_images',
                'total_downloaded_instances','total_downlinked_images', 'total_idle_instances', 'action_possible']]

    # length of data
    horizon = horizon - 1

    for n in range(1, horizon):
        solver_details = lines_cp_coord[n].split()
        start_time = int(solver_details[0])
        end_time = int(solver_details[1])



        z=start_time
        sat_time = satellite_data[z][0]
        sat_lat = satellite_data[z][1]
        sat_long = satellite_data[z][2]
        latitude = sat_lat
        longitude = sat_long

        print (sat_time, latitude, longitude)

        extracted_action = int(solver_details[2])
        memory_used = int(solver_details[4])
        pics_in_memory = float(solver_details[5])
        total_pics_count = int(solver_details[6])
        processed_images_in_memory = float(solver_details[7])
        total_processed_instances = int(solver_details[8])
        total_processed_images = float(solver_details[9])
        total_downloaded_instances = int(solver_details[10])
        total_downlinked_images = float(solver_details[11])
        total_idle_instances = int(solver_details[14])
        processed = str(solver_details[15])
        land_access = int(country_data_list[n][2])
        station_access = int(gnd_data_list[n][2])
        day_access = int(day_data_list[n][2])


        # Tabulate data.
        data.append(
            [start_time, end_time, latitude, longitude, land_access, station_access, day_access, extracted_action, n, memory_used, maximum_memory,
                 pics_in_memory, total_pics_count, processed_images_in_memory, total_processed_instances,total_processed_images,
                total_downloaded_instances,total_downlinked_images, total_idle_instances, processed])

    filename1 = filename + '/Day' + str(day) + '.txt'
    # Write data to file.
    file1 = open(filename1, 'w')
    df = pd.DataFrame(data)
    file1.writelines(df.to_string(header=False, index=False))
    file1.close()

    filename2 = filename + '/Day' + str(day) + '.xlsx'
    df = pd.DataFrame(data)
    writer = pd.ExcelWriter(filename2, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='data', index=False)
    # # df.drop(0, axis=1)
    writer.close()
    # with pd.ExcelWriter(filename2) as writer:
    #     df.to_excel(writer, index=False)

    read_file = pd.read_excel(filename2,skiprows=[0])
    print(read_file)
    filename3 = filename + "/Test.csv"
    # Write the dataframe object
    # into csv file
    read_file.to_csv(filename3 ,header=True, index=False)

main()