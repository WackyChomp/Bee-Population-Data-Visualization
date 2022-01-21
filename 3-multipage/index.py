import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app, server       # Connects to app.py
from apps import vg_sales, p_sales


# Landing Page on start up


# Links to different web pages
app.layout = html.Div([
    ddc.Location(id='url', refresh=False),            # reads URL in the browser (pathname is empty by default)
    html.Div([
        ddc.Link('Video Game Sales  |  ', href='/apps/vg_sales'),
        ddc.Link('Product Sales  |  ', href='/apps/p_sales')
    ], className="row"),

    html.Div(id="page-content", children=[])        # app pages are returned inside array based on callback
])

# Reading url pathname and returns web page file
@app.callback(Output(component_id='page-content', component_property='children'),
    [Input(component_id='url', component_property='pathname')])
def display_page(pathname):
    if pathname == '/apps/vg_sales':
        return vg_sales.layout
    if pathname == '/apps/':
        return 
    else:
        return "404 Link Error!"

#
if __name__ == '__main__':
    app.run_server(debug=False)