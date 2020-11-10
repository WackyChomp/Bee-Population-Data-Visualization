import dash          #version 1.17.0
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, All, State, MATCh, ALLSMALLER
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

    html.Div(id = 'container')      #graphs and components stored in this Div with children array
])

#-------------------------------------#



