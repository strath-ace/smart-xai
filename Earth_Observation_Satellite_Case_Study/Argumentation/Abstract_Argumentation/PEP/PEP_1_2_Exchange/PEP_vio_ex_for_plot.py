# ------------------Copyright (C) 2022 University of Strathclyde and Author ---------------------------------
# --------------------------------- Author: Cheyenne Powell -------------------------------------------------
# ------------------------- e-mail: cheyenne.powell@strath.ac.uk --------------------------------------------

# PEP calculation - 6th file, used to extract violations where conflicts occur and return data to be plotted.
# This function is called in the PEP 1_2_chart to generate a plot to provide a visual where PEP
# in breach of memory constraint
# ===========================================================================================================


def vio_check(vio, xi, yj, swap_1_2_summary):
    x1 = xi
    y1 = yj

    # Extract the position of these actions from the scheduled list where they overlap.
    index = [(a, swap_add.index(x1)) for a, swap_add in enumerate(swap_1_2_summary) if x1 in swap_add]
    index2 = [(a, swap_add.index(y1)) for a, swap_add in enumerate(swap_1_2_summary) if y1 in swap_add]

    # Use the extracted position data to cross-reference with the data containing the/
    # violation if there is a violation in memory.
    # If there is a violation, then extract that data to support grid.
    for v in range(0, len(index) - 1):
        pos1 = index[v][0]
        vio1 = swap_1_2_summary[pos1][2]
        for v2 in range(0, len(index2) - 1):
            pos2 = index2[v2][0]
            if pos1 == pos2:
                vio = vio1
            else:
                vio = 0

    return x1, y1, vio
