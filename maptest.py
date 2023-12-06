#Designing Data 
#Author: Johnathan Lee November December 2023
#Features of this program:
#1. processed data based on toronto water data
#2. processed data based on sars-cov-2 data
#3. 2 subplots 
#4. 1st subplot: line graph of sars-cov-2 concentration over time
#5. 2nd subplot: geo scatter plot of water treatment plants in toronto
import pandas as pd
import geopandas as gpd
import plotly.graph_objects as go
import csv
from plotly.subplots import make_subplots
fig = make_subplots(rows=1, cols=2,
                    specs=[[ {"type": "scatter"}, {"type": "scattermapbox"}]],
                    subplot_titles=("Sars-Cov-2 Concentration (RNA copies/L)", "Water Treatment Plants in Toronto"), 
                    )
fig['layout']['xaxis']['title']='Date'
fig['layout']['yaxis']['title']='RNA copies/L'

# Import data for first graph
#Minimal processing of data so used pandas library to read it without csv library 
data = pd.read_csv('waterlocation.csv')
from urllib.request import urlopen
# Import data for second graph 
with open('sarswaterdata.csv', newline='') as rawdata: 
    reader = csv.reader(rawdata)
    dataIn = list(reader)


i = 1
ashbridges = []
humber = []
highland = []
while i < len(dataIn):
    if dataIn[i][1] == "Ashbridges Bay":
        ashbridges.append([dataIn[i][0], dataIn[i][1], dataIn[i][2]])
    elif dataIn[i][1] == "Humber":
        humber.append([dataIn[i][0], dataIn[i][1], dataIn[i][2]])
    elif dataIn[i][1] == "Highland Creek":
        highland.append([dataIn[i][0], dataIn[i][1], dataIn[i][2]])


    i += 1
ashbridgesavg = []
humberavg = []
highlandavg = []
i = 0
count = 0
while i < len(ashbridges):
    sum1 = 0
    count = 0
    
    month = ashbridges[i][0].split("-")[1]
    year = ashbridges[i][0].split("-")[2]
    print(month)
    while i < len(ashbridges) and month == ashbridges[i][0].split("-")[1]:
         if ashbridges[i][2] != "":
            sum1 += float(ashbridges[i][2])
         count += 1
         i += 1
    average = sum1/count
    ashbridgesavg.append([month+' 20'+year, average, count])
    i += 1
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

df = pd.DataFrame(ashbridgesavg, columns = ['Date', 'Average', 'Count'])
df2 = pd.DataFrame(humberavg, columns = ['Date', 'Average', 'Count'])
df3 = pd.DataFrame(highlandavg, columns = ['Date', 'Average', 'Count'])

fig.add_trace(go.Scatter(x=df['Date'], y=df['Average'], name='Ashbridges Bay'), row=1, col=1)
fig.add_trace(go.Scatter(x=df2['Date'], y=df2['Average'], name='Humber'), row=1, col=1)
fig.add_trace(go.Scatter(x=df3['Date'], y=df3['Average'], name='Highland Creek'), row=1, col=1)

#***************************************#
#Second Graph

sizeref = 2 * max(data['Total Annual Flow']) / (40 ** 2)
fig.add_trace(go.Scattermapbox( 
    lat=data['lat'], 
    lon=data['long'], 
    mode='markers',
    
    marker=go.scattermapbox.Marker(
        size=data['Total Annual Flow'],
        sizemode='area',
        sizeref=sizeref,
        color=data['TSS'],
        colorscale='Thermal',
        showscale=True,
        colorbar=dict(title='Total Suspended Solids (mg/L)'),
       
    ), text=data['Plant'] + 'Treatment Plant Total Annual Flow m^3: ' + data['Total Annual Flow'].astype(str) + ' Total Suspended Solids mg/L: ' + data['TSS'].astype(str), hoverinfo='text', name='Geoscatter'), row=1 , col=2)
fig.update_legends(title_text='Water Treatment Plants')
fig.update_layout(title_text="Water Treatment Plants in Toronto: Water Volume and Quality", title_x=0.5)
fig.update_layout(showlegend=True, legend=dict(x=0.01, y=0.99))
fig.update_geos(fitbounds="locations", visible=True)

fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=8, mapbox_center = {"lat": 43.6532, "lon": -79.3832})
#show figure
fig.show()