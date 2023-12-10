#Designing Data 
#Author: Johnathan Lee November December 2023
#Features of this program:
#1. processed data based on toronto water data
#2. processed data based on sars-cov-2 data
#3. 2 subplots 
#4. 1st subplot: line graph of sars-cov-2 concentration over time
#5. 2nd subplot: geo scatter plot of water treatment plants in toronto
import pandas as pd
import plotly.graph_objects as go
import csv
from plotly.subplots import make_subplots

#***************************************#
#Subplot setup for part of C2
fig = make_subplots(rows=1, cols=2, #This specifies the number of rows and columns, 1 row means they will be next to each other two columns give the place for both graphs
                    specs=[[ {"type": "scatter"}, {"type": "scattermapbox"}]],#This specifies the type of graph for each subplot, as the scattermapbox needs special environment
                    subplot_titles=("Sars-Cov-2 Concentration (RNA copies/L)", "Water Treatment Plants in Toronto"), #creates titles for subplots
                    )
fig['layout']['xaxis']['title']='Date' #This sets the title for the x axis of the first subplot
fig['layout']['yaxis']['title']='RNA copies/L' #This sets the title for the y axis of the first subplot
#This adds the ttitles for the scatter plot as the scattermapbox does not need the titles



#***************************************#
#See for C2: Data Processing
# Import data for first graph
#Minimal processing of data so used pandas library to read it without csv library 
data = pd.read_csv('waterlocation.csv')
from urllib.request import urlopen
# Import data for second graph using csv library
with open('sarswaterdata.csv', newline='') as rawdata: 
    reader = csv.reader(rawdata)
    dataIn = list(reader)

#sort second graph data based on location into 3 lists
i = 1
ashbridges = []
humber = []
highland = []
#list structure: [date, location, concentration]
while i < len(dataIn):
    if dataIn[i][1] == "Ashbridges Bay":
        ashbridges.append([dataIn[i][0], dataIn[i][1], dataIn[i][2]])
    elif dataIn[i][1] == "Humber":
        humber.append([dataIn[i][0], dataIn[i][1], dataIn[i][2]])
    elif dataIn[i][1] == "Highland Creek":
        highland.append([dataIn[i][0], dataIn[i][1], dataIn[i][2]])


    i += 1

#monthly average for each location
#
ashbridgesavg = []
humberavg = []
highlandavg = []
#list structure: [date, average, count]
i = 0 #cycles through date
count = 0 #counts number of data points in a month for average calculation
while i < len(ashbridges):
    sum1 = 0 #sum of all data points in a month
    count = 0 #counts number of data points in a month for average calculation, resets to 0 for each month
    #data is stuctured as month-year
    month = ashbridges[i][0].split("-")[1] #splits date into month and year and takes month
    year = ashbridges[i][0].split("-")[2] #splits date into month and year and takes year
   #For each month while its the same month, add the data point to the sum and increment the count for average calculation
    while i < len(ashbridges) and month == ashbridges[i][0].split("-")[1]: #chekcs if month is the same
         if ashbridges[i][2] != "":#removes empty data points
            sum1 += float(ashbridges[i][2])#adds float data to the sum
         count += 1 #increments count
         i += 1 #increments i to move to next data point
    average = sum1/count #calculates average
    ashbridgesavg.append([month+' 20'+year, average, count]) #adds average to list, the "20" adds to the front of the two digit year
    i += 1 #increments i to move to next month in the first while loop


# repeats process for humber
i = 0 
count = 0
while i < len(humber):
    sum1 = 0
    count = 0
    
    month = humber[i][0].split("-")[1]
    year = humber[i][0].split("-")[2]
    print(month)
    while i < len(humber) and month == humber[i][0].split("-")[1]:
         if humber[i][2] != "":
            sum1 += float(humber[i][2])
         count += 1
         i += 1
    average = sum1/count
    humberavg.append([month+' 20'+year, average, count])
    i += 1

i = 0
count = 0
# repeats process for highland creek
while i < len(highland):
    sum1 = 0
    count = 0
    
    month = highland[i][0].split("-")[1]
    year = highland[i][0].split("-")[2]
    print(month)
    while i < len(highland) and month == highland[i][0].split("-")[1]:
         if highland[i][2] != "":
            sum1 += float(highland[i][2])
         count += 1
         i += 1
    average = sum1/count
    highlandavg.append([month+" 20"+year, average, count])
    i += 1
#***************************************#
#First Graph: Scatter graph
df = pd.DataFrame(ashbridgesavg, columns = ['Date', 'Average', 'Count'])
df2 = pd.DataFrame(humberavg, columns = ['Date', 'Average', 'Count'])
df3 = pd.DataFrame(highlandavg, columns = ['Date', 'Average', 'Count'])

fig.add_trace(go.Scatter(x=df['Date'], y=df['Average'], name='Ashbridges Bay'), row=1, col=1)
fig.add_trace(go.Scatter(x=df2['Date'], y=df2['Average'], name='Humber'), row=1, col=1)
fig.add_trace(go.Scatter(x=df3['Date'], y=df3['Average'], name='Highland Creek'), row=1, col=1)

#***************************************#
#Second Graph part of C2: Scattermapbox

# sizeref = 2 * max(data['Total Annual Flow']) / (40 ** 2) #scale the bubbles based on the total annual flow
# #reference size so data values dont have to be changed but size is still displayed larger
# #add trace function adds the graph to the figure
# fig.add_trace(go.Scattermapbox( #Uses geopandas to create a scattermapbox
#     lat=data['lat'], #creates loction based on lat and lon in the ata
#     lon=data['long'], 
#     mode='markers', #specifies the mode which is markers, meaning each point is a marker or in this case a bubble
    
#     marker=go.scattermapbox.Marker( #edits marker properties
#         size=data['Total Annual Flow'], #size is based on total annual flow this places the data for hover text
#         sizemode='area', #specifies the size mode as area, meaning the size is based on the area of the bubble
#         sizeref=sizeref, #calls the reference size from before
#         color=data['TSS'], #color is based on total suspended solids, a water quality indicator
#         colorscale='Thermal', #uses builtin "thermal" colorscale
#         showscale=True, #shows the scale, ensures reference area is shown
#         colorbar=dict(title='Total Suspended Solids (mg/L)'), #creates the title for the colorbar
#        #sets the hover text to display the plant name, total annual flow, and total suspended solids
#        #names the series "Geoscatter" so it can be referenced in the legend
#     ), text=data['Plant'] + 'Treatment Plant Total Annual Flow m^3: ' + data['Total Annual Flow'].astype(str) + ' Total Suspended Solids mg/L: ' + data['TSS'].astype(str), hoverinfo='text', name='Geoscatter'), 
#     row=1 , col=2)
# #adds it to the right subplot in the figure
# fig.update_legends(title_text='Water Treatment Plants') #adds the legend title
# fig.update_layout(title_text="Water Treatment Plants in Toronto: Water Volume and Quality", title_x=0.5) #adds the title for the entire figure
# fig.update_layout(showlegend=True, legend=dict(x=0.01, y=0.99)) #shows the legend and places it in the top left corner in the first subplot
# fig.update_geos(fitbounds="locations", visible=True) #fits the map to the locations of the water treatment plants and makes location names visible

# fig.update_layout(mapbox_style="carto-positron", #sets the mapbox style to carto-positron
#                   mapbox_zoom=8, mapbox_center = {"lat": 43.6532, "lon": -79.3832}) #sets the zoom and center of the map for when the figure is opened
# #show figure
fig.show()