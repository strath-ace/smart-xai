# ------------------ Copyright (C) 2022 University of Strathclyde and Author ---------------------------------
# --------------------------------- Author: Cheyenne Powell -------------------------------------------------
# ------------------------- e-mail: cheyenne.powell@strath.ac.uk --------------------------------------------

# File 3 b- This file is used for running all the SEP files in order
# ===========================================================================================================



from sep_comparison import initial_attack_calculation
from sep_data_sort import attack_summary
from violation_check import feasible_better
from code_memory_violation_for_plot import mem_vio
from Feasible_better_or_worse_chart import f_better_worse
from plot_results_infeasible import plo_res


def main():

    day = 3
    filename = '../SEP_Results/Day' + str(day)
    step = 0
    #step = 1
    while step !='7':
        step = input('Enter section or press 7 to exit: ')
        if step == '1':
            print(step)
            # File number 1 to extract data from solver schedule and create options where attacks can occur.
            initial_attack_calculation(day, filename)
            # step = '2'
        if step =='2':
            print(step)
            # SEP file number 2 - used to create the initial argumentation documents.
            attack_summary(day, filename)
            # step = '3'
        if step == '3':
            print(step)
            # feasible with a better objective or feasible with a worse objective - used for optimality.
            # NOT NEEDED FOR FEASIBILITY
            feasible_better(day, filename)
            # step = '4'
        if step == '4':
            print(step)
            # File 3 b- This file creates a summary following an attack of action a1 on other actions at selected time t,\
            # to the rest of the schedule.
            mem_vio(day, filename)
            # step = '5'
        if step == '5':
            print(step)
            # used to create 3 gantt charts to represent each action whether they are feasible better or feasible worse
            # based on the initial objective equation.
            f_better_worse(day, filename)
            # step = '6'
        if step == '6':
            print(step)
            # Function used for creating the gantt chart to show where all actions are scheduled to be executed and where\
            # the actions have attacked resulting with infeasible results.
            plo_res(day, filename)
            #step = 7

main()