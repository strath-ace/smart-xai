import pandas as pd
import datetime as dt

import plotly.express as px

day = 3

gantt_file1 = '../SEP_Results/Day/Gantt_plot_infeasible' + str(day) + '.png'

action_ap_path = '../SEP_Results/Day/Attack_summary_ap' + str(day) + '.txt'
action_ap_coord = open(action_ap_path, "r")
count_ap_coord = 0
# for loop to count the number of lines in file
for line in action_ap_coord:
    if line != "\n":
        count_ap_coord += 1
action_ap_coord.close()
print(count_ap_coord)
# load data line by line
action_ap_coord = open(action_ap_path, "r")
content_ap_coord = action_ap_coord.read()
lines_ap_coord = content_ap_coord.split('\n')

# load ar attack file
action_ar_path = '../SEP_Results/Day/Attack_summary_ar' + str(day) + '.txt'
action_ar_coord = open(action_ar_path, "r")
count_ar_coord = 0

# for loop to count the number of lines in file
for line in action_ar_coord:
    if line != "\n":
        count_ar_coord += 1
action_ar_coord.close()
print(count_ar_coord)

# load data line by line
action_ar_coord = open(action_ar_path, "r")
content_ar_coord = action_ar_coord.read()
lines_ar_coord = content_ar_coord.split('\n')

# load ad attack files
action_ad_path = '../SEP_Results/Day/Attack_summary_ad' + str(day) + '.txt'
action_ad_coord = open(action_ad_path, "r")
count_ad_coord = 0

# for loop to count the number of lines in file
for line in action_ad_coord:
    if line != "\n":
        count_ad_coord += 1
action_ad_coord.close()
print(count_ad_coord)

# load data line by line
action_ad_coord = open(action_ad_path, "r")
content_ad_coord = action_ad_coord.read()
lines_ad_coord = content_ad_coord.split('\n')

# load of attacks summary information
attack_path = '../SEP_Results/Day/Argumentation' + str(day) + '.txt'
attack_coord = open(attack_path, "r")
count_attack_coord = 0

# for loop to count the number of lines in file
for line in attack_coord:
    if line != "\n":
        count_attack_coord += 1
attack_coord.close()
print(count_attack_coord)

# load data line by line
attack_coord = open(attack_path, "r")
attack_cp_coord = attack_coord.read()
lines_attack_coord = attack_cp_coord.split('\n')


ap_attack = []
for i in range(1, count_ap_coord):
    ap_data = lines_ap_coord[i].split()

    start_time = int(ap_data[1])
    end_time = start_time + 5
    if ap_data[3] == '-' and ap_data[5] == 'Exceeded':
        Status = 'ap_Infeasible'

        memory_final_ap = ap_data[7]
        final_objective_ap = ap_data[8]

    else:
        memory_final_ap = 0
        final_objective_ap = 0
        Status = ''

    ap_attack.append([(dt.timedelta(seconds=(int(start_time)))), (dt.timedelta(seconds=(int(end_time)))), Status, memory_final_ap, final_objective_ap])

dc = pd.DataFrame({'Task': [(ap_attack[i][2]) for i in range(0, len(ap_attack))], 'Start': ['1970-01-01 ' + str(ap_attack[i][0]) for i in range(0, len(ap_attack))],
                   'Finish': ['1970-01-01 ' + str(ap_attack[i][1]) for i in range(0, len(ap_attack))], 'Resource': [(ap_attack[i][2]) for i in range(0, len(ap_attack))]})

ar_attack = []
for i in range(1, count_ar_coord):
    ar_data = lines_ar_coord[i].split()

    start_time = int(ar_data[1])
    end_time = start_time + 5
    if ar_data[3] == '-' and ar_data[5] == 'Exceeded':
        Status = 'ar_Infeasible'

        memory_final_ar = ar_data[7]
        final_objective_ar = ar_data[8]

    else:
        memory_final_ar = 0
        final_objective_ar = 0
        Status = ''

    ar_attack.append([(dt.timedelta(seconds=(int(start_time)))), (dt.timedelta(seconds=(int(end_time)))), Status, memory_final_ar, final_objective_ar])

dl = pd.DataFrame({'Task': [(ar_attack[i][2]) for i in range(0, len(ar_attack))], 'Start': ['1970-01-01 ' + str(ar_attack[i][0]) for i in range(0, len(ar_attack))],
                   'Finish': ['1970-01-01 ' + str(ar_attack[i][1]) for i in range(0, len(ar_attack))], 'Resource': [(ar_attack[i][2]) for i in range(0, len(ar_attack))]})

ad_attack = []
for i in range(1, count_ad_coord):
    ad_data = lines_ad_coord[i].split()
    # print(int(ad_data[1]))
    start_time = int(ad_data[1])
    end_time = start_time + 5
    if ad_data[3] == '-' and ad_data[5] == 'Exceeded':
        memory_final_ad = ad_data[7]
        final_objective_ad = ad_data[8]
        Status = 'ad_Infeasible'

    else:
        memory_final_ad = 0
        final_objective_ad = 0
        Status = ''

    ad_attack.append([(dt.timedelta(seconds=(int(start_time)))), (dt.timedelta(seconds=(int(end_time)))), Status, memory_final_ad, final_objective_ad])

ad_attack.append([(dt.timedelta(seconds=(int(0)))), (dt.timedelta(seconds=(int(0)))), 'ad_Infeasible', 0, 0])
dj = pd.DataFrame({'Task': [(ad_attack[i][2]) for i in range(0, len(ad_attack))], 'Start': ['1970-01-01 ' + str(ad_attack[i][0]) for i in range(0, len(ad_attack))],
                   'Finish': ['1970-01-01 ' + str(ad_attack[i][1]) for i in range(0, len(ad_attack))], 'Resource': [(ad_attack[i][2]) for i in range(0, len(ad_attack))]})

attack_summary = []

for i in range(15000, count_attack_coord - 800):
    all_data = lines_attack_coord[i].split()
    # ar_data = lines_ar_coord[i].split()

    start_time = int(all_data[0])
    end_time = start_time + 5
    S = all_data[4]
    if S == '0':
        # Take Images
        Status = 'ap'
    elif S == '1':
        # Process Images.
        Status = 'ar'
    elif S == '2':
        # Down-link Images.
        Status = 'ad'
    else:
        # Idle.
        Status = 'ae'

    attack_summary.append([(dt.timedelta(seconds=(int(start_time)))), (dt.timedelta(seconds=(int(end_time)))), Status, S])

df = pd.DataFrame({'Task': ['Schedule' for i in range(0, len(attack_summary))], 'Start': ['1970-01-01 ' + str(attack_summary[i][0]) for i in range(0, len(attack_summary))],
                   'Finish': ['1970-01-01 ' + str(attack_summary[i][1]) for i in range(0, len(attack_summary))], 'Resource': [(attack_summary[i][2]) for i in range(0, len(attack_summary))]})

# Arrange the results of plot to be represented in the order of ap, ar, ad, ae.
df_mapping = pd.DataFrame({'Resource': ['ap', 'ar', 'ad', 'ae'], })

sort_mapping = df_mapping.reset_index().set_index('Resource')

df['size_num'] = df['Resource'].map(sort_mapping['index'])

# Combining all data, df (actions scheduled), dc (action ap infeasible results), dl (action ar infeasible results) and dj (action ad infeasible results) to form 1 plot.
df2 = pd.concat([df.sort_values('size_num', ascending=True), dc.sort_values('Resource', ascending=True), dl.sort_values('Resource', ascending=True), dj.sort_values('Resource', ascending=True)])

# Colour chart created for each action.
discrete_map_resource = {'ap': '#FF6103', 'ar': '#FFD700', 'ad': '#0000EE', 'ae': '#000000', 'ar_Infeasible': '#8B4513', 'ap_Infeasible': '#FF0000', 'ad_Infeasible': '#008000'}

# Combine all data to form gantt chart.
fig1 = px.timeline(df2, x_start="Start", x_end="Finish", y="Resource", color="Resource", color_discrete_map=discrete_map_resource, hover_name="Task", color_discrete_sequence=px.colors.qualitative.Prism,
                   opacity=.7, range_x=None, range_y=None, template='plotly_white', height=1200, title="<b>Day</b>" + str(day))

fig1.update_layout(bargap=0.5, bargroupgap=0.1, xaxis_range=[df.Start.min(), df.Finish.max()],
                   xaxis=dict(showgrid=True, gridcolor='rgb(0,0,0)', side="bottom", tickmode='array', dtick="M1", tickformat="'%H:%M' \n", ticklabelmode="period", ticks="outside",
                              tickson="boundaries", tickwidth=.1, ticklen=20, tickfont=dict(family='Arial', size=40, color='black'), ),
                   yaxis=dict(title="", automargin=True, ticklen=5, showgrid=True, gridcolor='rgb(0,0,0)', showticklabels=True, tickfont=dict(family="Arial", size=50, color='black')),
                   legend=dict(orientation="h", yanchor="bottom", y=1, title="", xanchor="right", x=.9, font=dict(family="Arial", size=40, color="black")),
                   title=dict(font=dict(family="Arial", size=50, color="black")))

fig1.update_traces(marker_line_color='rgb(0,0,0)', marker_line_width=0.2, opacity=1)

# Store chart to file.
fig1.write_image(file=gantt_file1, format='png', scale=1, width=1800, height=800)
