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

    html.Div(id = 'container' , children = [])      #graphs and components stored in this Div with children list
])

#-------------------------------------#
#Callback 1: this is a set of inputs and outputs. Not functional
'''
The Inputs are strings

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
                    'type': 'dynamic-dpn-s',        #s = state
                    'index': n_clicks
                },
                options = [{'label': s, 'value': s} for s in np.sort(df['state'].unique())],
                multi = True,
                value = ["Andhra Pradesh", "Maharashtra"],
            ),

            dcc.Dropdown(         #4
                id = {
                    'type': 'dynamic-dpn-ctg',    #ctg = category
                    'index': n_clicks
                },
                options = [{'label': t, 'value': t} for t in ['caste', 'gender', 'state']],
                value = 'state',
                clearable = False
            ),

            dcc.Dropdown(         #5
                id = {
                    'type': 'dynamic-dpn-num',       #num = numerical
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
'''
The Input is a dictionary (In callback 1, they're strings)

The 'value' in component_property takes from 'index' in component_id

When the user changes the value of component_id, the callback is triggered

MATCH syncs up the index for Input and Output
'''
@app.callback(
    Output({'type': 'dynamic-graph', 'index': MATCH}, 'figure'),       #<--- matches the index of the input, not the graph
    [Input(component_id = {'type': 'dynamic-dpn-s', 'index': MATCH}, component_property= 'value'),
     Input(component_id = {'type': 'dynamic-dpn-ctg', 'index': MATCH}, component_property= 'value'),
     Input(component_id = {'type': 'dynamic-dpn-num', 'index': MATCH}, component_property= 'value'),
     Input({'type': 'dynamic-choice', 'index': MATCH}, 'value')]    #<--- same as above but with less naming / corresponds with the radio ID above
    )

def update_graph(s_value, ctg_value, num_value, chart_choice):
    print(s_value)
    dff = df[df['state'].isin(s_value)]

    if chart_choice == 'bar':
        dff = dff.groupby([ctg_value], as_index = False)[['detenues', 'under trial', 'convicts', 'others']].sum()
        fig = px.bar(dff, x = ctg_value, y = num_value)
        return fig      #refers to the Ouput in @app.callback
    
    elif chart_choice == 'line':
        if len(s_value) == 0:
            return {}
        else:
            dff = dff.groupby([ctg_value, 'year'], as_index = False)[['detenues', 'under trial', 'convicts', 'others']].sum()
            fig = px.line(dff, x = 'year', y = num_value, color = ctg_value)
            return fig

    elif chart_choice == 'pie':
        fig = px.pie(dff, names = ctg_value, values = num_value)
        return fig


#-------------------------------------#
if __name__ == '__main__':
    app.run_server(debug = True)
