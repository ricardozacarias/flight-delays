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

app = dash.Dash(__name__)

# open data
airports = pd.read_csv('airports_subset.csv', index_col=0)
flights = pd.read_csv('flights_subset.csv', index_col=0)

airport_options = []

map_layout = dict(showlegend = False, 
                  geo = dict(scope = 'north america',
                             projection = dict(type = 'azimuthal equal area'),
                             showland = True,
                             showcountries = True,
                             landcolor ='rgb(60, 60, 60)',
                             countrycolor ='rgb(204, 204, 204)'),
                  margin=dict(l=0,
                              r=0,
                              b=0,
                              t=0,
                              pad=0))

pie_layout = dict(showlegend=True)

map_marker = dict(size=10,
                  color="#e74c3c",
                  line=dict(width=1,
                            color='#000000'))

# define dropdown options
for airport in airports['NAME'].unique():
    airport_options.append({'label': airport, 'value': airports[airports['NAME'] == airport]['IATA'].values[0]})


# define layout
app.layout = html.Div(
    className="container scalable",
    children=[     
        html.Div(
            id="banner",
            className="banner",
            children=[
                html.Img(
                    src="https://fanart.tv/fanart/movies/813/hdmovieclearart/airplane-5124096339ae1.png",
                    id="airplane-image",
                    style={
                        "height": "200px",
                        "width": "auto",
                        "margin-top": "25px",
                        "margin-bottom": "25px",
                        "display":"block",
                        "margin-left": "auto",
                        "margin-right": "auto",})]), 
        
        html.Div([
            html.Div([
                html.Div(
                    id="origin-dropdown-title",
                    children=[
                        html.H6(html.Strong("Select origin")),
                    ],
                    style={
                        'textAlign': 'left',
                        'color': 'rgb(60, 60, 60)',
                }),
        
                dcc.Dropdown(
                    id='origin-dropdown',
                    options=airport_options,
                    placeholder='Select origin airport')],
                     
                className='pretty_container six columns'),
            
            html.Div([
                html.Div(
                    id="destination-dropdown-title",
                    children=[
                        html.H6(html.Strong("Select destination")),
                    ],
                    style={
                        'textAlign': 'left',
                        'color': 'rgb(60, 60, 60)',
                }),
                
                dcc.Dropdown(
                    id='destination-dropdown',
                    options=airport_options,
                    placeholder='Select destination airport')],
                
                className='pretty_container six columns')],
            
            className='row'),
        
        
        # MAP CONTAINER
        
        html.Div(
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
                'scrollZoom': False}),
            
            className='pretty_container',
        ),
        
        html.Div(id='route-text-output',
                 style={
                'margin-top':'25px',
                'textAlign': 'center',
                'color': 'rgb(60, 60, 60)'}),
        
        html.Div([
            html.Div(id='route-info',
                 className='pretty_container six columns'),
            html.Div(id='airline-pie',
                 className='pretty_container six columns'),
            ],
            className='row')
            ])

# CALLBACKS
# Text display route.
@app.callback(
    dash.dependencies.Output('route-text-output', 'children'),
    [dash.dependencies.Input('origin-dropdown', 'value'),
     dash.dependencies.Input('destination-dropdown', 'value')])

def update_route(origin, destination):
    if origin and destination:
        return dcc.Markdown(['#### Your Route', 'Departing from **{} ({})**'.format(airports[airports['IATA'] == origin]['NAME'].values[0], origin) + ', arriving at **{} ({})**'.format(airports[airports['IATA'] == destination]['NAME'].values[0], destination)])

# Update map with route selected
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
    
    cities = []
    
    if origin:
        cities += [flights[flights['Origin'] == origin]['OriginCityName'].unique()[0]]
        
    if destination:
        cities += [flights[flights['Dest'] == destination]['DestCityName'].unique()[0]]
    
    hover_text = ['<b>{route}</b><br>{airport_name}<br><b>City:</b> {city_name}'.format(route=text[i], airport_name= df_map['NAME'].values[i], city_name=cities[i]) for i in range(len(df_map['NAME'].values))]
    
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

@app.callback(
    dash.dependencies.Output('airline-pie', 'children'),
    [dash.dependencies.Input('origin-dropdown', 'value'),
     dash.dependencies.Input('destination-dropdown', 'value')])

def update_airline_pie(origin, destination):
       
    data = flights[(flights['Origin'] == origin) & (flights['Dest'] == destination)]['Reporting_Airline'].value_counts(normalize=True)
    
    # fix colors
    pie_marker = dict(line = dict(color='#000000', 
                                  width=1))
    
    #hover_text = 
    
    return dcc.Graph(
            id='airline-pie-chart',
            figure={
                'data': [{
                    'type': 'pie',
                    'values': data.values,
                    'labels': data.index,
                    'marker': pie_marker,
                    'hole': 0.5,
                    'hoverinfo':'text',
                    'text':'hello'}], 
                'layout': pie_layout,
                    }, 
            config={
            'displayModeBar': False,
            'scrollZoom': False})


@app.callback(
    dash.dependencies.Output('route-info', 'children'),
    [dash.dependencies.Input('origin-dropdown', 'value'),
     dash.dependencies.Input('destination-dropdown', 'value')])
    
def update_route_info(origin, destination):
    data = flights[(flights['Origin'] == origin) & (flights['Dest'] == destination)]
    
    return html.Div(
                    children=[
                        html.H6('Number of flights: ' + str(data.shape[0]))],      
                    style={'textAlign':'left'})
    

if __name__ == '__main__':
    app.run_server(debug=True)