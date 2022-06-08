# Solver
This folder contains the codes used for creating the heuristic schedule with a suggested input generated from the manually created schedule 
to guide the generation of the results. 

- **CPModel_with_Hint.py**
    - The initial file that contains the OR-Tools model and hints a solution from the manual schedule created
      to create an optimal solution. Due to the large data, a function was created to call the last stored results to reduce processing time.
    - This function then calls:
      - **file_recall**
        - Used call last read data in file n-1 or n depending on the day and if file already exists.
    - Following this, the solver is executed.
  - **CPSolver.py**
    - This function calls the OR-Tools solver and stores the values of actions determined into a file.
- **solver_test.py**
    - his function uses the solver with the manually created schedule to create an optimal schedule for the selected day
- **run_all_days.py**
  - This file is used to run all the codes for all the days entered. This will automatically run until the end last day has ended. 
  This will also plot all graphs required for each respective day, once a folder has been created.
  - It calls on all functions throughout all folders for the offline schedule.
