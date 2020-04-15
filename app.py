# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 23:32:52 2020

@author: Zaca
"""


# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

airports = pd.read_csv('us_airports.csv', index_col=0)

origin = 'LAX'
destination = 'JFK'

route = airports[(airports['IATA'] == origin) | (airports['IATA'] == destination)]



def route_fig(origin, destination):
    
    # customize hover text
    text = ['<b>{x}'.format(x=x) for x in route['NAME'].values]

    # define hover label properties
    hoverlabel = dict(bgcolor="white", 
                      font_size=12, 
                      font_family="Helvetica")

    # customize markers
    marker = dict(size=5,
                  color='rgb(255, 0, 0)',
                  line=dict(width=3,
                  color='rgba(68, 68, 68, 0)'))

    # customiz geo properties
    geo = dict(showland=True,
               landcolor='rgb(243, 243, 243)',
               countrycolor='rgb(204, 204, 204)',
               scope='north america',
               projection_type='azimuthal equal area')

    margin = {"r":0,"t":0,"l":0,"b":0}

    # create figure object
    fig = go.Figure()

    # add airport markers
    fig.add_trace(go.Scattergeo(lon=route['LONGITUDE'],
                                lat=route['LATITUDE'],
                                mode='markers',
                                marker=marker))

    # add route line between airports
    fig.add_trace(go.Scattergeo(lon=[route[route['IATA'] == origin]['LONGITUDE'].values[0], route[route['IATA'] == destination]['LONGITUDE'].values[0]],
                                lat=[route[route['IATA'] == origin]['LATITUDE'].values[0], route[route['IATA'] == destination]['LATITUDE'].values[0]],
                                mode='lines',
                                hoverinfo='text',
                                text=text,
                                line=dict(width=1,
                                          color='red')))
    # add layout configurations
    fig.update_layout(showlegend=False,
                      geo=geo,
                      hoverlabel=hoverlabel,
                      width=500,
                      height=300,
                      margin=margin)

    return dcc.Graph(figure=fig, 
                     config={'displayModeBar': False})


app.layout = html.Div(children=[
    
    html.H1(children='A dashboard for travellers.'),

    html.Div(children='''
        A dashboard for travellers.
    '''),
    
    # add route plot
    route_fig(origin, destination)])

if __name__ == '__main__':
    app.run_server(debug=True)