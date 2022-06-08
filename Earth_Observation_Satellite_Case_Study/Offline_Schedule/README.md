 
# Offline_Schedule
This folder contains the generated offline schedules both manually created solver and the 
solver. Here, the solver uses both the manual created schedule in combination with the satellites positions from the 
raw data previously mentioned.
  - ### Manual_Heuristic
    contains all the codes used for generating the schedules in addition, their respective graphs.
      - #### Manually_created_schedule
          This folder contains the codes used for creating the manual schedule
          The first is the main that is used for testing and generating results incorporating 3 functions
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