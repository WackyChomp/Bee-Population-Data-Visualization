import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app, server       # Connects to app.py


#
app.layout = html.Div([
    ddc.Location(id='url', refresh=False),
    html.Div([
        ddc.Link(''),
        ddc.Link('')
    ], className="row"),

    html.Div(id="page-content", children=[])
])

#
@app.callback(Output('page-content', 'children'),
    [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/':
        return 
    if pathname == '/apps/':
        return 
    else:
        return "404 Link Error!"

#
if __name__ == '__main__':
    app.run_server(debug=False)