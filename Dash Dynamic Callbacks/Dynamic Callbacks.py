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

