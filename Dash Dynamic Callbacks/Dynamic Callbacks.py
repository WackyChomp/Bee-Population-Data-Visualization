import dash          #version 1.17.0
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, ALL, State, MATCH, ALLSMALLER
import plotly.express as px
import pandas as pd
import numpy as np

#read csv
df = pd.read_csv("India_Caste.csv")

#rename column names
df.rename(columns = {'under_trial': 'under trial' , 'state_name': 'state'}, inplace = True)

app = dash.Dash(__name__)         #initiate the app

#-------------------------------------#
#Application Layout
'''
In basic callbacks, you must have the necessary components in layout before you introduce them in the callback

All you need is the layout with the button and Div
'''
app.layout = html.Div([        
    html.Div(children = [
        html.Button('Add Chart', id = 'add-chart', n_clicks = 0),
    ]),

    html.Div(id = 'container')      #graphs and components stored in this Div with children list
])

#-------------------------------------#
#Callback 1: this is a set of inputs and outputs. Not functional
'''
In Input, when n_clicks is triggered it triggers 
callback and display_graphs function gets triggered

In State, it saves the information of 
children when callback is triggered

The id in children is mandatory for dynamic callbacks
'''

@app.callback(
    Output('container', 'children'),
    [Input('add-chart', 'n_clicks')],
    [State('container', 'children')]
)

def display_graphs(n_clicks, div_children):
    new_child = html.Div(
        style = {
            'width': '45%',
            'display': 'inline-block',
            'outline': 'thin lightgrey solid',
            'padding': 10
            },
        
        children = [
            dcc.Graph(            #1
                id = {
                    'type': 'dynamic-graph',
                    'index': n_clicks
                    },
                figure = {}
                ),

            dcc.RadioItems(       #2
                id = {
                    'type': 'dynamic-choice',
                    'index': n_clicks
                    },
                options = [{'label': 'Bar Chart', 'value': 'bar'},
                           {'label': 'Line Chart', 'value': 'line'},
                           {'label': 'Pie Chart', 'value': 'pie'}],
                value = 'bar',
                ),
            
            dcc.Dropdown(         #3
                id = {
                    'type': 'dynamic-dpn-s',
                    'index': n_clicks
                    },
                options = [{'label': s, 'value': s} for s in np.sort(df['state'].unique())],
                multi = True,
                value = ["Andhra Pradesh", "Maharashtra"],
                ),

            dcc.Dropdown(         #4
                id = {
                    'type': 'dynamic-dpn-ctg',
                    'index': n_clicks
                    },
                options = [{'label': t, 'value': t} for t in ['caste', 'gender', 'state']],
                value = 'state',
                clearable = False
                ),

            dcc.Dropdown(         #5
                id = {
                    'type': 'dynamic-dpn-num',
                    'index': n_clicks
                    },
                options = [{'label': u, 'value': u} for u in ['detenues', 'under trial', 'convicts', 'others']],
                value = 'convicts',
                clearable = False
                )
            ]
        )
    div_children.append(new_child)
    return div_children         #add html.Div every click

#-------------------------------------#
#Callback 2: Creating the interactive aspect

@app.callback(
    Output({'type': 'dynamic-graph', 'index': MATCH}, 'figure'),
    [Input(component_id = {'type': 'dynamic-dpn-s', 'index': MATCH}, component_property= 'value'),
     Input(component_id = {'type': 'dynamic-dpn-ctg', 'index': MATCH}, component_property= 'value'),
     Input(component_id = {'type': 'dynamic-dpn-num', 'index': MATCH}, component_property= 'value'),
     Input({'type': 'dynamic-choice', 'index': MATCH}, 'value')]
    )
