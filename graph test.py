import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, date2num
import time
import plotly as py
import plotly.figure_factory as ff
import plotly.express as px
import datetime as dt
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objs as go


daily_path = 'C:/Users/User/Documents/PhD/ESA/Satellite data/Sentinel 2/Sentinel2A/daily_schedule.txt'

daily_coord = open(daily_path, "r")
line_count_coord = 0
for line in daily_coord:
    if line != "\n":
        line_count_coord += 1
daily_coord.close()

daily_coord = open(daily_path, "r")
# print(line_count)
node_count_coord = line_count_coord
content_coord = daily_coord.read()
lines_coord = content_coord.split('\n')



memory_states = 'C:/Users/User/Documents/PhD/ESA/Satellite data/Sentinel 2/Sentinel2A/memory_states.txt'

memory_coord = open(memory_states, "r")
memory_count_coord = 0
for line in memory_coord:
    if line != "\n":
        memory_count_coord += 1
memory_coord.close()

memory_coord = open(memory_states, "r")
# print(line_count)
memory_count_coord = memory_count_coord
memory_coord = memory_coord.read()
memory_coord = memory_coord.split('\n')

memory_land_list=[]
memory_end_time=[]
memory_start_time =[]
memory_summary = {}


for i in range(0, memory_count_coord):
    memory_details = memory_coord[i].split()
    #print(daily_details[3])

    if memory_details[2] == '0':
        action = 'inactive'
    elif memory_details[2] == '1':
        action = 'take_pictures'
    elif memory_details[2] == '2':
        action='Process_Image'
    elif memory_details[2] == '3':
        action = 'Calibrate'
    elif memory_details[2] == '4':
        action = 'Dump'
        #Task= 'Job_Land'
    memory_land_list.append([memory_details[0], memory_details[1], memory_details[2], action,memory_details[3],memory_details[6]])
    # memory_time.append(memory_details[0])
    # memory_end_time.append(memory_details[2])

dl=pd.DataFrame({'Task':['Job_%i'for i in range (0, len(memory_land_list))],'Start':['1970-01-01 '+str(memory_land_list[i][0]) for i in range (0, len(memory_land_list))],
                 'Finish':['1970-01-01 '+str(memory_land_list[i][1])for i in range (0, len(memory_land_list))],'Resource':[(memory_land_list[i][3]) for i in range(0,len(memory_land_list))]})


daily_land_list=[]
duration_time=[]
start_time =[]
job_summary = {}

for i in range(0, node_count_coord):
    daily_details = lines_coord[i].split()
    #print(daily_details[3])

    if daily_details[3] == 'Process_images'or daily_details[3] == 'Matera' or \
            daily_details[3] == 'Eumetsat'or daily_details[3] =='PrudhoeBay' or daily_details[3] == 'Svalbard':
        Land = 'Ground_stations'
    elif daily_details[3] == 'Penumbra':
        Land = 'night'
    else:
        Land='Land'
        #Task= 'Job_Land'
    daily_land_list.append([daily_details[0], daily_details[1], daily_details[2], Land])

df=pd.DataFrame({'Task':['Job_%i'for i in range (0, len(daily_land_list))],'Start':['1970-01-01 '+str(daily_land_list[i][0]) for i in range (0, len(daily_land_list))],
                 'Finish':['1970-01-01 '+str(daily_land_list[i][1])for i in range (0, len(daily_land_list))],'Resource':[(daily_land_list[i][3]) for i in range(0,len(daily_land_list))]})

#df=pd.DataFrame({'Task':['Job_%i'for i in range (0, len(daily_land_list))],'Start':[((dt.timedelta(seconds=float(daily_land_list[i][0]))))for i in range (0, len(daily_land_list))],
#                 'Finish':[(str(dt.timedelta(seconds=float(daily_land_list[i][1]))))for i in range (0, len(daily_land_list))],'Resource':[(daily_land_list[i][3]) for i in range(0,len(daily_land_list))]})
    #,'Time':(str(dt.timedelta(seconds=(start_ints[i]))), (Demands_mem[i], Actives_List[i])) for i in range (0, len(daily_land_list))]})
#df = pd.DataFrame([dict(Task="Job %i", Start= str(dt.timedelta(seconds=float(daily_land_list[i][0]))), Finish=str(dt.timedelta(seconds=float(daily_land_list[i][1]))), Resource=daily_land_list[i][3]) for i in range(0,len(daily_land_list))])

# df['Start'] = pd.to_datetime(df['Start'])
# df['Finish'] = pd.to_datetime(df['Finish'])
# #fig, ax = plt.subplots()
#
# myFmt = DateFormatter("%H:%M:%S")print
#ax.xaxis.set_major_formatter(myFmt)
df2=pd.concat([dl,df])
fig = px.timeline(df2, x_start="Start", x_end="Finish", y="Resource", color="Resource", hover_name="Task"
                  , color_discrete_sequence= px.colors.qualitative.Prism
                  , opacity=.7
#                   , text="Task"
                  , range_x=None
                  , range_y=None
                  , template='plotly_white'
                  , height=1200
#                   , width=1500

                  , title ="<b>TimeStamp</b>"
#                   , color=colors
                 )
#fig.add_bar(dl, x_start="Start", x_end="Finish", y="Resource", color="Resource")




fig.update_layout(
    bargap=0.5
    , bargroupgap=0.1
    , xaxis_range=[df.Start.min(), df.Finish.max()]
    , xaxis=dict(
        showgrid=True
        #, rangeslider_visible=True
        , side="bottom"
        , tickmode='array'
        , dtick="M1"
        , tickformat="'%H:%M:%S' \n"
        , ticklabelmode="period"
        , ticks="outside"
        , tickson="boundaries"
        , tickwidth=.1
        #, layer='below traces'
        , ticklen=20
        , tickfont=dict(
            family='Old Standard TT, serif', size=24, color='gray')
        , )

    , yaxis=dict(
        title=""
        , autorange="reversed"
        , automargin=True
        #         ,anchor="free"
        , ticklen=10
        , showgrid=True
        , showticklabels=True
        , tickfont=dict(
            family='Old Standard TT, serif', size=16, color='gray'))

    , legend=dict(
        orientation="h"
        , yanchor="bottom"
        , y=1.1
        , title=""
        , xanchor="right"
        , x=1
        , font=dict(
            family="Arial"
            , size=14
            , color="black"))
)
fig.update_traces( #marker_color='rgb(158,202,225)'
                   marker_line_color='rgb(8,48,107)'
                   ,marker_line_width=0.5, opacity=0.95)




#plt.gcf().autofmt_xdate()
fig.show()