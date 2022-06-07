- # Manual_Heuristic
Contains all the files and codes used for generating the schedules in addition, their respective graphs.

Namely:
1. [Manually_created_schedule](#Manually_created_schedule)
2. [Solver](#Solver)
3. [graph_plot_code](#graph_plot_code)


## Manually_created_schedule
This folder contains the codes used for creating the manual schedule
The first is the main that is used for testing and generating results incorporating 3 main functions with each containing their support functions
- **test_manual_schedule.py** <br/> -
       Uses the 3 functions  below:\
    1. **Manual_heuristic.py** \
            Uses the function below.\
            - **Manual_Processing_Time.py**\
    2. **Heuristic_memory_calculation.py**\
       Uses the 2 functions below.\
         - **Memory_calculation_support_1.py**\
         - **Memory_calculation_support_2.py**\
    3. **Manual_binary_data.py**\
       Uses the function below\.
         - **start_end_points_data.py**


## Solver
This folder contains the codes used for creating the heuristic schedule with a suggested input generated from the manually created schedule 
to guide the generation of the results.       

## Graph_plot_code
This folder contains all the files linked required or plotting the graphs after the results have been generated.

Namely:
 - **call_plots_test.py**
 - **gantt_plot.py**
 - **manual_memory_plot.py**
 - **Solver_plot.py**
