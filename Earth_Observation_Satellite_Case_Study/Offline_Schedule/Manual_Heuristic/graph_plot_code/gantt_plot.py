# This file creates the gantt plots and saves the image
# creates the gantt plot for the manual schedule, the positions of the satellite as well as the solver

import pandas as pd
import plotly.express as px


def gantt_plot(day, memory_land_list_binary, daily, constraint_land_list, gantt_file):
    daily_land_list = []
    daily_coord = open(daily, "r")
    line_count_coord = 0
    for line in daily_coord:
        if line != "\n":
            line_count_coord += 1
    daily_coord.close()

    daily_coord = open(daily, "r")
    node_count_coord = line_count_coord
    content_coord = daily_coord.read()
    lines_coord = content_coord.split('\n')

    for i in range(0, node_count_coord):
        daily_details = lines_coord[i].split()

        if daily_details[3] == 'Matera' or daily_details[3] == 'Eumetsat' or daily_details[3] == 'PrudhoeBay' or daily_details[3] == 'Svalbard':
            Position = 'Ground_stations'
        elif daily_details[3] == 'Penumbra' or daily_details[3] == 'Penumbra Shade':
            Position = 'night'

        elif daily_details[3] != 'Process_images' and (daily_details[3] != 'Matera' or daily_details[3] != 'Eumetsat' or daily_details[3] != 'PrudhoeBay' or daily_details[3] != 'Svalbard'):
            # and any(e[3] == daily_details[3] for e in country_access(1, 'Dec', 2020, 'All')):
            Position = 'Land'

        else:
            Position = ''

        if Position != '':
            daily_land_list.append([daily_details[0], daily_details[1], daily_details[2], Position])

    df = pd.DataFrame({'Task': ['Job_%i' for _ in range(0, len(daily_land_list))], 'Start': ['1970-01-01 ' + str(daily_land_list[i][0]) for i in range(0, len(daily_land_list))],
                       'Finish': ['1970-01-01 ' + str(daily_land_list[i][1]) for i in range(0, len(daily_land_list))], 'Resource': [(daily_land_list[i][3]) for i in range(0, len(daily_land_list))]})

    dl = pd.DataFrame({'Task': ['Job_%i' for _ in range(0, len(memory_land_list_binary))], 'Start': ['1970-01-01 ' + str(memory_land_list_binary[i][0]) for i in range(0, len(memory_land_list_binary))],
                       'Finish': ['1970-01-01 ' + str(memory_land_list_binary[i][1]) for i in range(0, len(memory_land_list_binary))],
                       'Resource': [(memory_land_list_binary[i][2]) for i in range(0, len(memory_land_list_binary))]})

    dc = pd.DataFrame({'Task': ['Job_%i' for _ in range(0, len(constraint_land_list))], 'Start': ['1970-01-01 ' + str(constraint_land_list[i][0]) for i in range(0, len(constraint_land_list))],
                       'Finish': ['1970-01-01 ' + str(constraint_land_list[i][1]) for i in range(0, len(constraint_land_list))], 'Resource': [(constraint_land_list[i][2]) for i in range(0, len(constraint_land_list))]})

    df2 = pd.concat([dl, df, dc])
    fig1 = px.timeline(df2, x_start="Start", x_end="Finish", y="Resource", color="Resource", hover_name="Task", color_discrete_sequence=px.colors.qualitative.Prism, opacity=.7, range_x=None, range_y=None,
                       template='plotly_white', height=1200, title="<b>Day</b>" + str(day))

    fig1.update_layout(bargap=0.5, bargroupgap=0.1, xaxis_range=[df.Start.min(), df.Finish.max()],
                       xaxis=dict(showgrid=True, side="bottom", tickmode='array', dtick="M1", tickformat="'%H:%M:%S' \n", ticklabelmode="period", ticks="outside", tickson="boundaries", tickwidth=.1, ticklen=20,
                                  tickfont=dict(family='Arial', size=30, color='black'), ),
                       yaxis=dict(title="", automargin=True, ticklen=10, showgrid=True, showticklabels=True, tickfont=dict(family="Arial", size=30, color='black')),
                       legend=dict(orientation="h", yanchor="bottom", y=1.1, title="", xanchor="right", x=1, font=dict(family="Arial", size=20, color="black")),
                       title = dict(font=dict(family="Arial", size=40, color="black")))


    fig1.update_traces(marker_line_color='rgb(8,48,107)', marker_line_width=0.5, opacity=0.95)

    fig1.write_image(file=gantt_file, format='png', scale=1, width=2500, height=1250)
