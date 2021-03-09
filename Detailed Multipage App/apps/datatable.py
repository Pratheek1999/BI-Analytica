import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html 
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pyodbc 
conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=MSI-PRATHEEK;'
                      'Database=PBS2_Kolhapur;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()

sql_query = pd.read_sql_query('SELECT D.Pod_number, D.Pod_date, D.Pod_Amount, S.State_Code, S.State_Name, P.Place_Code, P.Place_Name, I.Party_ID, I.Party_Name, B.Branch_code, B.Branch_Name, L.Bill_Code, L.Bill_No, L.Bill_Date, L.Party_ID, L.Bill_Amount FROM State S INNER JOIN Place P ON S.State_Code = P.State_Code INNER JOIN Pod D ON P.Place_Code = D.Place_Code INNER JOIN Branch B ON D.Branch_ID = B.Branch_ID INNER JOIN Bill L ON D.Bill_Code = L.Bill_code INNER JOIN Party I ON D.Party_ID = I.Party_ID',conn)


    # -------------------------------------------------------------------------------------
# App layout
app = dash.Dash(__name__, prevent_initial_callbacks=True) # this was introduced in Dash version 1.12.0

# Sorting operators (https://dash.plotly.com/datatable/filtering)
app.layout = html.Div([
    html.H1('Data Table', style={"textAlign": "center"}),

    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in sql_query.columns],
        data=sql_query.to_dict('records'),  # the contents of the table
        editable=True,              # allow editing of data inside all cells
        filter_action="native",     # allow filtering of data by user ('native') or not ('none')
        sort_action="native",       # enables data to be sorted per-column by user or not ('none')
        sort_mode="single",         # sort across 'multi' or 'single' columns
        column_selectable="multi",  # allow users to select 'multi' or 'single' columns
        row_selectable="multi",     # allow users to select 'multi' or 'single' rows
        row_deletable=True,         # choose if user can delete a row (True) or not (False)
        selected_columns=[],        # ids of columns that user selects
        selected_rows=[],           # indices of rows that user selects
        page_action="native",       # all data is passed to the table up-front or not ('none')
        page_current=0,             # page number that user is on
        page_size=6,                # number of rows visible per page
        style_cell={                # ensure adequate header width when text is shorter than cell's text
            'minWidth': 95, 'maxWidth': 95, 'width': 95
        },
        style_cell_conditional=[    # align text columns to left. By default they are aligned to right
            {
                'if': {'column_id': c},
                'textAlign': 'left'
            } for c in ['country', 'iso_alpha3']
        ],
        style_data={                # overflow cells' content into multiple lines
            'whiteSpace': 'normal',
            'height': 'auto'
        }
    ),

    html.Br(),
    html.Br(),
    html.Div(id='bar-container')

])

# -------------------------------------------------------------------------------------
# Create bar chart
@app.callback(
    Output(component_id='bar-container', component_property='children'),
    [Input(component_id='table', component_property="derived_virtual_data"),
     Input(component_id='table', component_property='derived_virtual_selected_rows'),
     Input(component_id='table', component_property='derived_virtual_selected_row_ids'),
     Input(component_id='table', component_property='selected_rows'),
     Input(component_id='table', component_property='derived_virtual_indices'),
     Input(component_id='table', component_property='derived_virtual_row_ids'),
     Input(component_id='table', component_property='active_cell'),
     Input(component_id='table', component_property='selected_cells')]
)
def update_bar(all_rows_data, slctd_row_indices, slct_rows_names, slctd_rows,
               order_of_rows_indices, order_of_rows_names, actv_cell, slctd_cell):
    print('***************************************************************************')
    print('Data across all pages pre or post filtering: {}'.format(all_rows_data))
    print('---------------------------------------------')
    print("Indices of selected rows if part of table after filtering:{}".format(slctd_row_indices))
    print("Names of selected rows if part of table after filtering: {}".format(slct_rows_names))
    print("Indices of selected rows regardless of filtering results: {}".format(slctd_rows))
    print('---------------------------------------------')
    print("Indices of all rows pre or post filtering: {}".format(order_of_rows_indices))
    print("Names of all rows pre or post filtering: {}".format(order_of_rows_names))
    print("---------------------------------------------")
    print("Complete data of active cell: {}".format(actv_cell))
    print("Complete data of all selected cells: {}".format(slctd_cell))

    dff = pd.DataFrame(all_rows_data)

    # used to highlight selected countries on bar chart
    colors = ['#7FDBFF' if i in slctd_row_indices else '#0074D9'
              for i in range(len(dff))]

    if "Place_Name" in dff and "Pod_Amount" in dff:
        return [
            dcc.Graph(id='bar-chart',
                      figure=px.bar(
                          data_frame=dff,
                          x="Place_Name",
                          y='Pod_Amount',
                          labels={"Pod_Amount": "Total Sales"}
                      ).update_layout(showlegend=False, xaxis={'categoryorder': 'total ascending'})
                      .update_traces(marker_color=colors, hovertemplate="<b>%{y}%</b><extra></extra>")
                      )
        ]


# -------------------------------------------------------------------------------------
# Highlight selected column
@app.callback(
    Output('table', 'style_data_conditional'),
    [Input('table', 'selected_columns')]
)
def update_styles(selected_columns):
    return [{
        'if': {'column_id': i},
        'background_color': '#D2F3FF'
    } for i in selected_columns]


# -------------------------------------------------------------------------------------


if __name__ == '__main__':
    app.run_server(debug=True)