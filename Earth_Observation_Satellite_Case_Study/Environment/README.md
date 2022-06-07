# Earth Observation Case study - Environment 

This folder contains all the code and raw data of an Earth Observation (EO) satellite to read and 
generate data regarding the satellites coordinates.

The **_Data_** file contains the following:

* Ground stations text file - contains the coordinates of the satellite when the ground stations are within range for communicating.

* Land text file - contains all the coordinates and times when the satellite has a visual of land.

* Light Shade exposure text file - contains all the data when the satellite is within an eclipse of the earth.

Additionally, There are 6 files used to read from the Data folder.

1. **environment_data_to_solver.py** - This function is used to send satellites position data to the function
solver test.

2. **ground_station_access.py** -
This function is used to extract all the selected ground station access for an Earth Observation satellite
for selected day from the txt file

3. **Land_visibility.py** - This function is used for generating land visibility data for a selected day 
extracted from the text file.    

4. **Shade_exposure.py** - This file is used for generating data where light/shade exposures occur over a selected day.

5. **start_end_points_data.py** - This file is used for determining the start and end times for each day.

6. **test_environment_data.py** - Used for testing. This function is used for extracting the data of satellites position
for a selected day.
