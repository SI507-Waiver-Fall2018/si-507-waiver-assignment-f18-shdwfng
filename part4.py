# Imports -- you may add others but do not need to
import plotly.plotly as py
import plotly.graph_objs as go

# Code here should involve creation of the bar chart as specified in instructions
# And opening / using the CSV file you created earlier with noun data from tweets

xdata = []
ydata = []

file= open('noun_data.csv', 'r')

for line in file:
	data = line.split(',')
	xdata.append(data[0])
	ydata.append(data[1][:-1])

xdata = xdata[1:]
ydata = ydata[1:]

godata = [go.Bar(x=xdata,y=ydata)]

layout = go.Layout(width=800, height=640)
fig = go.Figure(data=godata, layout=layout)

py.image.save_as(fig, filename='part4_viz_image.png')