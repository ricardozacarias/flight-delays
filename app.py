# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 23:32:52 2020

@author: Zaca
"""


# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

def example_graph():
    
     return dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )


app.layout = html.Div(children=[
    html.H1(children='A dashboard for travellers.'),

    html.Div(children='''
        A dashboard for travellers.
    '''),
    example_graph()

])

if __name__ == '__main__':
    app.run_server(debug=True)