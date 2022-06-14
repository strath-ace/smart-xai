## Abstract Argumentation (AA)

AA s a technique used to provide information, highlighting where conflicts of elements may occur in a system. 
This project contains the AA methods used to support with providing explanations to the End User of an EO satellite schedule.
The satellite schedule has 3 main actions and a fourth created when no other actions have occurred. 
Each of these actions as described in [EO case study](/./README.md#Earth-Observation-Case-study).

The four actions are:
1. **Taking of images** - given a label '0' and 'a1' throughout the codes.
2. **Processing** of the taken image - given the label '1' and 'a2' throughout the codes.
3. **Down-linking** of the taken and processed image - given the label '2' and 'a3' throughout the codes.
4. **Idle time** - created when no other actions could be executed. This was given the label '-1' and 'a4' throughout the codes.


Within AA, 2 techniques were investigated.

- [Single Exchange Property (SEP)](#Single-Exchange-Property-(SEP))
- [Pairwise Exchange Property (PEP)](#Pairwise-Exchange-Property-(PEP))

### Single Exchange Property (SEP)

SEP is a technique used to see the effects of a schedule if an action was replaced with another.
SEP in this application, the concept was applied to a satellite schedule derived by a CP solver.

Note, the 4th action idle, can only be attacked by other actions for SEP as it has no value. 

Within SEP, there are 7 codes that are used within:

Note: Points 1 and 2 **must** be executed in this order.
1. **sep_comparison.py** - used to extract data from the solver schedule and create options where attacks can occur.
2. **sep_data_sort.py** - used to create the initial argumentation documents.
3. Can be executed in any order.
   1. **violation_check.py** - used to calculate the objective each time SEP is used and determine if the result is feasible better or
   feasible with a worse objective.
   2. **code for memory violation plot.py** - This code creates a summary following an attack of action a1 on other actions at selected time t,
   to the rest of the schedule. This time can be altered.

#### SEP Graphs
3 different files were created or plotting each graph

1. **SEP_plot.py** - used for creating the line plot with the variance in memory due to an attack on action 1 comparing to the generated schedule 
   by the solver, can be used for actions 2 and 3. slight mods required.
2. **SEP_plot_all_data.py** - similar to point 1, however, the number of images in memory for each of the 3 main actions are included in the graph. Please note,
    the number of down-linked images resets after every 15000 seconds.
3. **plot_results_infeasible.py** - used for creating the gantt chart to show where all actions are scheduled to be executed and where the actions have attacked resulting in infeasible results
4. **Feasible_better_or_worse_chart.py** - used to create 3 gantt charts to represent each action whether they are feasible better or feasible worse based on the initial objective equation.

### Pairwise Exchange Property (PEP)

PEP in this case is the swapping of any two actions throughout a schedule to observe the effects on a schedule. This generates a solution and provides when the
solution is feasible or infeasible.

There is 1 main code that is reliant on 3 functions namely:

1. **PEP_swap.py** - function used to calculate for feasibility with first number cascaded to the second number.\
   Within this file, several functions are called:
   1. **PEP_Feasible_check.py** - checks for feasibility with pair exchanges by checking which action of the 2 appears first in the schedule,
       to then swap and calculate the memory using:
      1. **PEP_calc.py** -  function used to calculate for feasibility with first number cascaded to the second number. 
      However, to check the constraints of the main problem, the following code was derived:
         1. **constraints_considered_add2.py** - used to check if the second action exchange can be completed without violating the constraints.

#### PEP Graphs
The following codes were used to support providing results to the end user.
1. **PEP_1_2_chart.py** - This code was used to plot an nxm matrix plot showing where every 2 action can be replaced at every instance throughout a scheduled day displaying where conflicts occur (times are adjustable).
   This file uses the following code:
   1. **PEP_vio_ex_for_plot** -  used to extract violations where conflicts occur and return data to be plotted. 
