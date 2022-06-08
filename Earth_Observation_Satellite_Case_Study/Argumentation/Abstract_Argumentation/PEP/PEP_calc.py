# ------------------Copyright (C) 2022 University of Strathclyde and Author ---------------------------------
# --------------------------------- Author: Cheyenne Powell -------------------------------------------------
# ------------------------- e-mail: cheyenne.powell@strath.ac.uk --------------------------------------------

# PEP calculation 3 - function used to calculate for feasibility with first number cascaded to the second number.
# Note: Actions were given numbers idle - '-1', image taking - '0', processing - '1', and down-linking - '2'.
# ===========================================================================================================

from Earth_Observation_Satellite_Case_Study.Argumentation.Abstract_Argumentation.PEP.constraints_considered_add2 \
    import attack_calculation


def pep_action_a(a, m, i, ma1, ma2, ma3, count_coord, lines_cp_coord, lines_attack_coord, addrx,
                 a2, m_max, add1, add2):
    mi_a = m
    violation1 = ''
    start_time2 = 0
    mi_a2 = 0

    # Check which swapped action comes first and use action with the lower address value to calculate the memory
    # up to the address of the second action.
    if add2 > add1:  # attack add2 with add1

        # For the first address.
        for n in range(add1, add2):

            start_time2 = lines_cp_coord[i + n - add1].split()[0]

            s_1 = lines_attack_coord[i + n - add1].split()[4]

            # Check if the position marker is at the first address then assign the new memory. Already found from SEP.
            if n == add1:
                # New memory for action swap.
                mi_a = m

            # Otherwise, calculate the new memory based on the action in queue.
            else:
                if s_1 == '0':
                    mi_a = mi_a + ma1
                elif s_1 == '1':
                    mi_a = mi_a + ma2
                elif s_1 == '2':
                    mi_a = mi_a + ma3
                else:
                    mi_a = mi_a

            # Check for memory violation.
            if mi_a > m_max or mi_a <= 0:
                violation1 = 'Exceeded'
                a = '-'
                # If memory is exceeded then break the function.
                break

        # Function called to check calculations for attack of action at address 2.
        mi_a2 = attack_calculation(a2, addrx, mi_a, lines_cp_coord, lines_attack_coord)

        # Checks the action at the second address for memory breach.
        for n in range(add2, count_coord - 1):

            # Check if memory is exceeded.
            if mi_a2 > m_max or mi_a2 <= 0:
                violation1 = 'Exceeded'
                a = '-'

                # Terminate function.
                break

            # Checks each action next in the schedule with the alternate memory created.
            if n >= count_coord - i:
                s_1 = lines_attack_coord[n].split()[4]
                start_time2 = lines_cp_coord[n].split()[0]
            else:
                s_1 = lines_attack_coord[i + n - add2].split()[4]
                start_time2 = lines_cp_coord[i + n - add2].split()[0]

            # IF the position marker is at address 2 then use the updated memory for the action.
            if n == add2:
                mi_a2 = mi_a2

            # Checks the next action in the queue to generate an alternate memory value.
            else:
                if s_1 == '0':
                    mi_a2 = mi_a2 + ma1
                elif s_1 == '1':
                    mi_a2 = mi_a2 + ma2
                elif s_1 == '2':
                    mi_a2 = mi_a2 + ma3
                else:
                    mi_a2 = mi_a2

            # Check if memory is exceeded.
            if mi_a2 > m_max or mi_a2 <= 0:
                violation1 = 'Exceeded'
                a = '-'
                # Terminates the function if memory is breached
                break

            # Proceed.
            else:
                if n == count_coord - 1:
                    violation1 = 'Not_exceeded'
                else:
                    violation1 = 'Not_exceeded'
                a = '-'

    return i, a, violation1, start_time2, mi_a, mi_a2
