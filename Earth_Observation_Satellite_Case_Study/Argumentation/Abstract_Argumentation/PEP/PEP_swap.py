# ------------------ Copyright (C) 2022 University of Strathclyde and Author ---------------------------------
# --------------------------------- Author: Cheyenne Powell -------------------------------------------------
# ------------------------- e-mail: cheyenne.powell@strath.ac.uk --------------------------------------------

# PEP calculation 1 - used to initiate swapping between actions.
# Note: Actions were given numbers idle - '-1', image taking - '0', processing - '1', and down-linking - '2'.
# ===========================================================================================================

import pandas as pd
from Earth_Observation_Satellite_Case_Study.Argumentation.Abstract_Argumentation.PEP.PEP_Feasible_check import \
    pep_check_swap


def PEP_swap(lines_attack_coord, day, filename, att_path, datastart, dataend):
    filename1 = filename + '/Attack_swap_a' + str(day) + '.txt'

    x = []
    y = []
    x_action = []
    y_action = []

    # Extract all matching data for times of action execution and action execution itself
    for i in range(datastart, dataend):
        x_y_data = lines_attack_coord[i].split()
        x_time = int(x_y_data[0])
        y_time = int(x_y_data[0])
        S_x_data = int(x_y_data[4])
        S_y_data = int(x_y_data[4])

        mi = x_y_data[5]

        x.append(x_time)
        y.append(y_time)
        x_action.append(S_x_data)
        y_action.append(S_y_data)

    x1_coordinates = []
    y1_coordinates = []
    mem_violation = []
    file1 = open(filename1, 'w')
    final_list = [['i', 'start_time', 'swap_location', 'S', 'a1', 'a2', 'a3', 'idle', 'mi', 'violation', 'mem_vio',
                   'time_of_incident', 'mem1', 'mem2', 'mem3']]

    # Create an (n x m) matrix with each action scheduled and check if they both can be swapped once they aren't
    # the same action.
    # Meaning can any 2 actions be swapped?
    # rows
    for i in range(len(x) - 1):
        # initialize list
        if i > 0:
            final_list = []

        # columns
        for j in range(len(y) - 1):

            action_swap1 = x_action[i]
            action_swap2 = y_action[j]

            # If statement to enable exchange of action 0 and 1.
            if [x_action[i], y_action[j]] == [0, 1]:
                x1 = x[i]
                y1 = y[j]
                addr1 = i
                addr2 = j

                # Add data containing whether there is a violation/breach in memory.
                final_list.append(pep_check_swap(day, att_path, datastart, addr1, addr2, action_swap1, action_swap2))

            # If statement to enable exchange of action 1 and 0.
            elif [x_action[i], y_action[j]] == [1, 0]:
                x1 = x[i]
                y1 = y[j]
                addr1 = i
                addr2 = j

                # Add data containing whether there is a violation/breach in memory.
                final_list.append(pep_check_swap(day, att_path, datastart, addr1, addr2, action_swap1, action_swap2))

            # If statement to enable exchange of action 0 and -1.
            elif [x_action[i], y_action[j]] == [0, -1]:
                x1 = x[i]
                y1 = y[j]
                addr1 = i
                addr2 = j

                # Add data containing whether there is a violation/breach in memory.
                final_list.append(pep_check_swap(day, att_path, datastart, addr1, addr2, action_swap1, action_swap2))

            # If statement to enable exchange of action -1 and 0.
            elif [x_action[i], y_action[j]] == [-1, 0]:
                x1 = x[i]
                y1 = y[j]
                addr1 = i
                addr2 = j

                # Add data containing whether there is a violation/breach in memory.
                final_list.append(pep_check_swap(day, att_path, datastart, addr1, addr2, action_swap1, action_swap2))

            # If statement to enable exchange of action 0 and 2.
            elif [x_action[i], y_action[j]] == [0, 2]:
                x1 = x[i]
                y1 = y[j]
                addr1 = i
                addr2 = j

                # Add data containing whether there is a violation/breach in memory.
                final_list.append(pep_check_swap(day, att_path, datastart, addr1, addr2, action_swap1, action_swap2))

            # If statement to enable exchange of action 2 and 0.
            elif [x_action[i], y_action[j]] == [2, 0]:
                x1 = x[i]
                y1 = y[j]
                addr1 = i
                addr2 = j

                # Add data containing whether there is a violation/breach in memory.
                final_list.append(pep_check_swap(day, att_path, datastart, addr1, addr2, action_swap1, action_swap2))

            # If statement to enable exchange of action 1 and -1.
            elif [x_action[i], y_action[j]] == [1, -1]:
                x1 = x[i]
                y1 = y[j]
                addr1 = i
                addr2 = j

                # Add data containing whether there is a violation/breach in memory.
                final_list.append(pep_check_swap(day, att_path, datastart, addr1, addr2, action_swap1, action_swap2))

            # If statement to enable exchange of action -1 and 1.
            elif [x_action[i], y_action[j]] == [-1, 1]:
                x1 = x[i]
                y1 = y[j]
                addr1 = i
                addr2 = j

                # Add data containing whether there is a violation/breach in memory.
                final_list.append(pep_check_swap(day, att_path, datastart, addr1, addr2, action_swap1, action_swap2))

            # If statement to enable exchange of action 1 and 2.
            elif [x_action[i], y_action[j]] == [1, 2]:
                x1 = x[i]
                y1 = y[j]
                addr1 = i
                addr2 = j

                # Add data containing whether there is a violation/breach in memory.
                final_list.append(pep_check_swap(day, att_path, datastart, addr1, addr2, action_swap1, action_swap2))

            # If statement to enable exchange of action 2 and 1.
            elif [x_action[i], y_action[j]] == [2, 1]:
                x1 = x[i]
                y1 = y[j]
                addr1 = i
                addr2 = j

                # Add data containing whether there is a violation/breach in memory.
                final_list.append(pep_check_swap(day, att_path, datastart, addr1, addr2, action_swap1, action_swap2))

            # If statement to enable exchange of action 2 and -1.
            elif [x_action[i], y_action[j]] == [2, -1]:
                x1 = x[i]
                y1 = y[j]
                addr1 = i
                addr2 = j

                # Add data containing whether there is a violation/breach in memory.
                final_list.append(pep_check_swap(day, att_path, datastart, addr1, addr2, action_swap1, action_swap2))

            # If statement to enable exchange of action -1 and 2.
            elif [x_action[i], y_action[j]] == [-1, 2]:

                x1 = x[i]
                y1 = y[j]
                addr1 = i
                addr2 = j

                # Add data containing whether there is a violation/breach in memory.
                final_list.append(pep_check_swap(day, att_path, datastart, addr1, addr2, action_swap1, action_swap2))

            else:
                x1 = x_action[i]
                y1 = y_action[j]
                mem_vio = -1
            x1_coordinates.append(x1)
            y1_coordinates.append(y1)

        # Store the first row (headings of columns) to file.
        if final_list[0][0] == 'i' and len(final_list) > 0:
            file1 = open(filename1, 'a')
            df = pd.DataFrame(final_list)
            file1.writelines(df.to_string(header=False, index=False))

        # Store each individual row to file with their respective heading.
        else:
            file1 = open(filename1, 'a')
            file1.write("\n")
            df = pd.DataFrame(final_list)
            file1.writelines(df.to_string(header=False, index=False))
