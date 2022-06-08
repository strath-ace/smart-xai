# Manually_created_schedule
  This folder contains the codes used for creating the manually generated schedule by the end user.
  The first is the main that is used for testing and generating results incorporating 3 functions
  with each containing their support functions.
   - test_manual_schedule.py - used for testing purposes <br/> -
       Uses the 3 functions  below:
        1. **Manual_heuristic.py** \
            Function used for generating the schedule-
              1. Prevents' an images from being taken when in the shade.
              2. Where actions overlap  a weight is given to the actions to prioritise 1 over the other, thus durations\
                 for the lower prioritised action is altered.
              3. Generates the final schedule.\
           Within this function, it uses: \
           - **Manual_file_recall.py** - used to check if files for previous day exist and forward the last generated
           results from the previous day to the current day
           - **Manual_Processing_Time.py** - to generate the processing times based on the gaps between the actions within a given day.
        2. **Heuristic_memory_calculation.py**\
           This function is used for generating 2 lists 1 with time in hh: mm: ss and the other in milliseconds based 
     on the position of the satellite with their respective actions.\
            Uses the 2 functions below:
             - **Memory_calculation_support_1.py** - used for calculating the memory from the generated manual schedule over a given day
             - **Memory_calculation_support_2.py** - used for calculating the total memory from the generated manual schedule over a given day
           and determines whether the activity is to occur as well as calculate the total number of instances for each activity
        3. **Manual_binary_data.py**\
           This function is used for generating the boolean data to be sent to the solver and for generating the gantt chart
           Uses the function below.
             - **start_end_points_data.py** - Can be found in Environment folder - used for determining the start and end times for each day.
           