import pandas as pd
import plotly.express as px     #(version 4.12.0)
import dash         #(version )
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)      #starts the app

#--------------------------------------------------#
#imports cvs data into pandas for cleaning

df = pd.read_csv("Bee Stats")         #data that you plan to use

df = df.groupby(['State', 'ANSI', 'Affected by', 'Year', 'state_code'])[['Pct of Colonies Impacted']].mean()
#select columns and obtain the average percent of colonies impacted

df.reset_index(inplace = True)
print(df[:5])

#--------------------------------------------------#
#Application Layout: Dash compenents / graphs / dropdown / checkbox / html

app.layout = html.Div([
    html.H1("Bee Web Application Dashboards with Dash", style = {'text-align': 'center'}),

    dcc.Dropdown(id = "slct_year",
        options = [
            #users see the lable / dropdown looks at value
            {"label": "2015", "value": 2015},
            {"label": "2016", "value": 2016},
            {"label": "2017", "value": 2017},
            {"label": "2018", "value": 2018},
            {"label": "2019", "value": 2019}],
        multi = False,
        value = 2015,
        style = {'width': "40%"}
        ),
    
    html.Div(id = 'output_container', children = []),

    html.Br(),

    dcc.Graph(id = 'bee_map', figure = {})
])

#--------------------------------------------------#