import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pathlib
from app import app

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

# Dataset reading
dfv = pd.read_csv(DATA_PATH.joinpath("PBS2_Kolhapur_Schema.csv"))  # GregorySmith Kaggle

# Page layout
layout = html.Div([
    html.H1('Yearly Client Sales', style={"textAlign": "center"}),

    html.Div([
        html.Div([
            html.Pre(children="Year", style={"fontSize": "150%"}),
            dcc.Dropdown(
                id='year-dropdown', value='2016', clearable=False,
                options=[{'label': x, 'value': x} for x in sorted(dfv["Sales_Year"].unique())]
            )

        ], className='six columns'),

        html.Div([
            html.Pre(children="State", style={"fontSize": "150%"}),
            dcc.Dropdown(
                id='state-dropdown', value='MAHARASHTRA', clearable=False,
                options=[{'label': x, 'value': x} for x in sorted(dfv["State_Name"].unique())]
            )

        ], className='six columns'),
    ], className='row'),

    dcc.Graph(id='my-bar', figure={}),
])


#################################################################


# Dropdown callbacks
@app.callback(
    Output(component_id='my-bar', component_property='figure'),
    [Input(component_id='year-dropdown', component_property='value'),
     Input(component_id='state-dropdown', component_property='value')]
)

# Linking the values from DB(csv)
def display_value(year_chosen, state_chosen):
    dfv_fltrd = dfv[(dfv['Sales_Year'] == year_chosen) &
                    (dfv["State_Name"] == state_chosen)]

    fig = px.bar(dfv_fltrd, x='Party_Name', y='Bill_Amount', color='Place_Name')
    fig = fig.update_yaxes(tickprefix="₹", ticksuffix="")
    return fig
