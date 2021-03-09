import dash_core_components as dcc
import dash_html_components as html
from dash import dash
from dash.dependencies import Input, Output
import dash_auth

# Connect to main app.py file
from app import app
from app import server


# Connect to your app pages
from apps import yearly_client_sales, global_sales, datatable

auth = dash_auth.BasicAuth(
app,{'pratheek': '1234',
'general': '1234'})


# Creating links to navigate between pages
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Data Table | ', href='/apps/datatable'),
        dcc.Link('Client Sales | ', href='/apps/yearly_client_sales'),
        dcc.Link('US Clients', href='/apps/global_sales'),
    ], className="row"),
    html.Div(id='page-content', children=[])
])


# Connecting the navigation links & the pages together
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/yearly_client_sales':
        return yearly_client_sales.layout
    if pathname == '/apps/global_sales':
        return global_sales.layout
    if pathname == '/apps/datatable':
        return datatable.app.layout

    else:
        return "404 Page Error! Please choose a link"


if __name__ == '__main__':
    app.run_server(debug=False)
