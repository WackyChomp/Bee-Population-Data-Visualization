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
#Callback: Connects the Plotly graphs with Dash Components

@app.callback(
    [Output(component_id = 'output_container', component_property = 'children'),
    Output(component_id = 'bee_map', component_property = 'figure')],

    [Input(component_id = 'slct_year', component_property = 'value')],    #this input goes into the output above
    )


def update_graph(option_slctd):          #refers to input component_property / what user selects for dropdown input appears here
    print(option_slctd)            #good practice to print out values and data type
    print(type(option_slctd))


    container = "The user chose the year: {}".format(option_slctd)


    dff = df       #df = data frame
    dff = dff[dff["Year"] == option_slctd]     #takes the year row based on what the user selected. Default is based on application layout dropdown
    dff = dff[dff["Affected by"] == "Varroa_mites"]


    #Make choropleth graph with Plotly Express
    fig = px.choropleth(
        data_frame = dff,
        locationmode = "USA-states",
        locations = "state_code",
        scope = "usa",
        color = "Pct of Colonies Impacted",
        hover_data = ["State", "Pct of Colonies Impacted"],
        color_continuous_scale = px.colors.sequential.YlOrRd,
        labels = {'Pct of Colonies Impacted': "Pct of Bee Colonies"},
        template = "plotly_dark"
    )


    return container, fig          #what is returned here goes into output

#--------------------------------------------------#

if __name__ == '__main__':
    app.run_server(debut = True)