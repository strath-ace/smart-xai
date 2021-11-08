# smart-xai - Google OR-Tools Sentinel-2A Case study

The structure of this folder is shown below<br/>

Sentinel 2A Case Study<br/>

 - ## Environment
      - Data
          - Land
          - Ground Stations
          - Day/Night
      - test_environment_data.py and environment_data_to_solver.py uses the following codes
          - Land_visibility.py
              - start_end_points_data.py
          - ground_station_access.py
              - start_end_points_data.py
          - Shade_exposure.py
             - start_end_points_data.py

 - ## Offline_Schecule
      - Manual_Heuristic
          - Manually_created_schedule
               - test_manual_schedule.py 
                    - Manual_heuristic.py
                        - Manual_Processing_Time.py
                    - Heuristic_memory_calculation.py
                         - Memory_calculation_support_1.py
                         - Memory_calculation_support_2.py
                    - Manual_binary_data.py
                         - start_end_points_data.py
        
           - Solver
             - solver_test.py
                - environment_data_to_solver.py
                - Manual_binary_data.py
                - CPModel_with_Hint.py
                   - file_recall.py
                - CPSolver.py
                   - file_recall.py
          
           - graph_plot_code
               - call_plots_test.py
                   - manual_memory_plot.py
                   - Solver_plot.py
                   - gantt_plot.py
     
     |-Results
          |-Day 1
              |-Solver
              |-Garphs
          |-Day 2
              |-Solver
              |-Graphs
