# smart-xai 
# Earth Observation Case study

This project creates both a simple manual schedule and an updated schedule using Google-OR-Tools using the initially 
created schedule, thus in combination generating a heuristic OPTIMAL schedule. 
In addition, Abstract Argumentation used in support of XAI has been implemented. 

The schedules are both created based on the positions of an Earth Observation (EO) Satellite in LEO over a period 
of 6 months, between December 2020 and May 2021.

The aim of this project is to generate a schedule for an EO satellite, to capture images of land only when in sunlight 
and down-link data when access to ground station is possible which can occur in either the shade/sunlight. 
In order to down-link data, the satellite has to process the images and as a result processing can occur any time.

When processing images however, the satellite will retain the images until down-linking has occurred in case the
processed images becomes corrupt, the original file is there to be reprocessed.

The amount of images processed and downlink is based on the hardware limitations of the satellite and as a result, 
depending on the on-board processing capabilities, it can take several processing instances to complete an image and 
several down-linking instances to send 1 image after it has been processed.

The structure of this folder is shown below


 - ## Environment
    This folder contains both the raw data of the satellites' positions and the initial code that
     was used to create the manual schedule as stated above.
      - ### Data
        The data in this folder, contains the raw text files extracted from the AGI STK software of the 
        satellites position and exposure when over land.
          - Land
          - Ground_Stations
          - Day/Night
      - ### 'test_environment_data.py' and 'environment_data_to_solver.py' 
          The 2 functions listed above, 1 is for testing and the other is for pushing the data to another function.
          These files are used to look for the complete land list or specific country including all ground station access and shade/sun exposure.<br/>
      
          <br/>The start and end times for each day varies as day 1 is on the 1st of December at 11:00:00 and any other day starts at 00:00:1.<br/><br/>
          - Land_visibility.py <br/>
             Uses the function below.
              - start_end_points_data.py
          - ground_station_access.py<br/>
             Uses the function below.
              - start_end_points_data.py
          - Light_Shade_exposure.py<br/>
             Uses the function below.
             - start_end_points_data.py

 - ## Offline_Schecule
    This folder contains the generated offline schedules both manually created solver and the 
    solver. Here, the solver uses both the manual created schedule in combination with the satellites positions from the 
    raw data previously mentioned.
      - ### Manual_Heuristic
        contains all the codes used for generating the schedules in addition, their respective graphs.
          - #### Manually_created_schedule
              This folder contains the codes used for creating the manual schedule
              The first is the main that is used for testing and generating results encorporating 3 functions
              with each containing their support functions
               - test_manual_schedule.py<br/> 
                   Uses the 3 functions  below.
                    - Manual_heuristic.py
                        Uses the function below.
                        - Manual_Processing_Time.py
                    - Heuristic_memory_calculation.py
                       Uses the 2 functions below.
                         - Memory_calculation_support_1.py
                         - Memory_calculation_support_2.py
                    - Manual_binary_data.py
                       Uses the function below.
                         - start_end_points_data.py
        
          - #### Solver
            This folder generates the final schedules using the manual results in a boolean format
            in combination with the satellites positions using the constraints
            
            - solver_test.py
            
               Uses the 4 functions below.
               - environment_data_to_solver.py
               - Manual_binary_data.py
               - CPModel_with_Hint.py
                 Uses the function below.
                  - file_recall.py
               - CPSolver.py
                 Uses the function below.
                  - file_recall.py
            - Run_all_days.py
                Uses all the codes and generates all the schedules over x period of days
                carrying over all the data from each day to the next as well as plotting all the graphs 
                for each respective day. 
                This code initially creates the folder and files for each day if they don't exist to generate results
          
          - #### graph_plot_code
              - call_plots_test.py
                  - manual_memory_plot.py
                  - Solver_plot.py
                  - gantt_plot.py
     
      - ### Results - folders automatically created per daily result
           - #### Day 1
               - Solver
               - Garphs
           - #### Day 2
               - Solver
               - Graphs
