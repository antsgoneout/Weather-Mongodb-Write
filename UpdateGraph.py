__author__ = 'DuthoitA'


from pymongo import *
import plotly.plotly as py
from plotly.graph_objs import *

def update_plotly():
#
# open database
    try:
        #c = Connection(host="192.168.1.186", port=27017)
        c = Connection(host="localhost", port=27017)
    except:
        print('Could not connect to MongoDB')
        exit()
    dbname=c["db"]
    assert dbname.connection == c
    xx = []
    yy0 = []
    yy1 = []

#
# get last 7 records
    datacursor=dbname.weather.find({}, {"Observation Time": 1, "Temperature": 1, "Visibility": 1}).sort('_id', DESCENDING).limit(99)

    for recordsets in datacursor:
        #print(recordsets["Observation Time"], recordsets["Temperature"])
        xx.append(recordsets["Observation Time"])
        yy0.append(recordsets["Temperature"])
        yy1.append(recordsets["Visibility"])

    #print(xx)
    #print(yy0, yy1)

    trace0 = Scatter(
        x = xx,
        y = yy0,
        name = 'Temperature',
        line = Line(shape='spline')
    )

    trace1 = Scatter(
        x = xx,
        y = yy1,
        name = 'Visibility',
        yaxis = 'y2',
        line = Line(shape='spline')
    )
    layout = Layout(
        title='Odiham Weather',
        annotations=Annotations(
            #x=2,
            #y=5,
            #xref='x',
            #yref='y',
            #text='Annotation Text'
            #showarrow=True,
            #arrowhead=7
            #ax=0,
            #ay=-40
            ),
        yaxis=YAxis(
            title='Temperature Degrees C'
        ),
        yaxis2=YAxis(
            title='Visbility metres',
            titlefont=Font(
                color='rgb(148, 103, 189)'
            ),
            tickfont=Font(
                color='rgb(148, 103, 189)'
            ),
            overlaying='y',
            side='right'
        )
    )
    data = Data([trace0, trace1])
    fig = Figure(data=data, layout=layout)
    unique_url = py.plot(fig, filename='Odiham Weather', auto_open=False)
    print(trace0, trace1)

    print(unique_url)