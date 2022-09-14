# ------------------ Copyright (C) 2022 University of Strathclyde and Author ---------------------------------
# --------------------------------- Author: Cheyenne Powell -------------------------------------------------
# ------------------------- e-mail: cheyenne.powell@strath.ac.uk --------------------------------------------

# File - This file is used for running all the PEP files in order
# ===========================================================================================================
import os
from PEP_swap import PEP_swap
from Earth_Observation_Satellite_Case_Study.Argumentation.Abstract_Argumentation.PEP.PEP_1_2_Exchange.PEP_1_2_chart import PEP_1_2_chart

# Only 2 files are needed to execute the others

def main():
    day = 3
    filename = '../PEP_Results/Day' + str(day)
    att_path = '../SEP_Results/Day' + str(day)

    # Load of attacks summary information.
    attack_path = att_path + '/Argumentation' + str(day) + '.txt'
    if os.path.isfile(attack_path):
        print('File ' + attack_path + ' exists')
    else:
        print('Please run SEP file - Run_all_SEP step #2 - Sep_data_sort_attack_summary')
        print('File ' + attack_path + ' does not exist')
        return ()

    attack_coord = open(attack_path, "r")
    count_attack_coord = 0

    # For loop to count the number of lines in file.
    for line in attack_coord:
        if line != "\n":
            count_attack_coord += 1
    attack_coord.close()
    print(count_attack_coord)

    # Load data line by line.
    attack_coord = open(attack_path, "r")
    attack_cp_coord = attack_coord.read()
    lines_attack_coord = attack_cp_coord.split('\n')

    solver_path = '../../../Offline_Schedule/Results_with max(pic,proc,down)/Day ' + str(day) + \
                  '/Solver/Optimized_results' + str(day) + '.txt'

    solver_coord = open(solver_path, "r")
    count_coord = 0

    # For loop to count the number of lines in file.
    for line in solver_coord:
        if line != "\n":
            count_coord += 1
    solver_coord.close()
    print(count_coord)
    # load data line by line
    solver_coord = open(solver_path, "r")
    content_cp_coord = solver_coord.read()
    lines_cp_coord = content_cp_coord.split('\n')
    # create a new folder 'Day #' and sub folders if the folder doesn't exist
    if os.path.isdir(filename):
        print('File ' + filename + ' exists')
    else:
        os.makedirs(filename)

    # datastart = 1
    # dataend = count_attack_coord - 1
    datastart = 1500
    dataend = count_attack_coord - 2270
    print(datastart,dataend)

    # The commented section below are used for testing start and end times for data testing
    #########################################
    # datastart = 15000                     #
    # dataend = count_attack_coord-2270     #
    # dataend = count_attack_coord-2100     #
    #########################################


    step = 0
    #step = 1
    while step !='3':
        step = input('Enter section or press 3 to exit: ')

        if step == '1':
            print(step)
            # PEP calculation 1 - used to initiate swapping between actions.
            # Note: Actions were given numbers idle - '-1', image taking - '0', processing - '1', and down-linking - '2'.
            PEP_swap(lines_attack_coord, day, filename, att_path, datastart, dataend)
            step = '2'
        if step == '2':
            print(step)

            # To initiate the range of data for data plot, can be altered as data set can be large.
            # Start and end points are used for plot ranges minimum datastart can be 1 and dataend = count_attack_coord - 2
            datastart = 1590
            dataend = 1605
            # This file is used to plot an nxm matrix plot showing where every 2 action can be replaced at every/
            # instance throughout a scheduled day displaying where conflicts occur.
            PEP_1_2_chart(day, filename, att_path, datastart, dataend, lines_attack_coord)
            step = '3'
main()