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
airport_options = []

map_layout = dict(showlegend = False, 
                  geo = dict(scope='north america',
                             projection=dict(type='azimuthal equal area'),
                             showland = True,
                             showcountries = True,
                             landcolor='rgb(60, 60, 60)',
                             countrycolor='rgb(204, 204, 204)'),
                  margin=dict(l=0,
                              r=0,
                              b=0,
                              t=0,
                              pad=0))

map_marker = dict(size=10,
                  color="#e74c3c",
                  line=dict(width=1,
                            color='#000000'))

# define dropdown options
for airport in airports['NAME'].unique():
    airport_options.append({'label': airport, 'value': airports[airports['NAME'] == airport]['IATA'].values[0]})


# define layout
app.layout = html.Div([
    
    dcc.Dropdown(
        id='origin-dropdown',
        options=airport_options,
        placeholder='Select origin airport'),
    
    html.Div(id='origin-text-output'),
    
    dcc.Dropdown(
        id='destination-dropdown',
        options=airport_options,
        placeholder='Select destination airport'),
    
    html.Div(id='destination-text-output'),
    
    dcc.Graph(
        id='map',
        
        figure={
            'data': [{
                'lat': [None, None],
                'lon': [None, None],
                'type': 'scattergeo'
            }, 
                {
                'lat': [None, None],
                'lon': [None, None],
                'type': 'scattergeo'
            }],
            'layout': map_layout,
            },
        
        config={
        'displayModeBar': False,
        'scrollZoom': False})
    ])

# text display origin airport
@app.callback(
    dash.dependencies.Output('origin-text-output', 'children'),
    [dash.dependencies.Input('origin-dropdown', 'value')])

def update_origin(value):
    if value:
        return 'Departing from {} ({})'.format(airports[airports['IATA'] == value]['NAME'].values[0], value)

@app.callback(
    dash.dependencies.Output('destination-text-output', 'children'),
    [dash.dependencies.Input('destination-dropdown', 'value')])

def update_destination(value):
    if value:
        return 'Arriving at {} ({})'.format(airports[airports['IATA'] == value]['NAME'].values[0], value)

@app.callback(
    dash.dependencies.Output('map', 'figure'),
    [dash.dependencies.Input('origin-dropdown', 'value'),
     dash.dependencies.Input('destination-dropdown', 'value')]
)

# update map based on the dropdown airports
def update_map(origin, destination):
    
    origin_airport = airports[(airports['IATA'] == origin)]   
    destination_airport = airports[(airports['IATA'] == destination)]
    
    df_map = pd.concat([origin_airport, destination_airport])
    
    text = ['Origin', 'Destination']
    hover_text = ['<b>{}:<br>{}'.format(text[i], df_map['NAME'].values[i]) for i in range(len(df_map['NAME'].values))]
    
    return {
        'data': [{
            'lat': df_map['LATITUDE'],
            'lon': df_map['LONGITUDE'],
            'marker': map_marker,
            'type': 'scattergeo',
            'hoverinfo': 'text',
            'text': hover_text
        },
            {
            'lat': df_map['LATITUDE'],
            'lon': df_map['LONGITUDE'],
            'mode': 'lines',
            'type': 'scattergeo',
            'line': dict(width=2,
                         color="#e74c3c"),
            'hoverinfo': 'skip'
        }],
        
        'layout': map_layout
    }


if __name__ == '__main__':
    app.run_server(debug=True)