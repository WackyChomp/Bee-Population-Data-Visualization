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



#--------------------------------------------------#