import dash
from dash import dcc, html, Input, Output, State, callback, dash_table
import pandas as pd

from DataStructures.TableTypes import TableType, table_types
import DataOperations.MySQL as MySQL
from DataOperations import TableOperations
import config


# TODO
#  - Modul should talk to View Edit module

dash.register_page(__name__)

layout = html.Div([
    html.H1('Data processing page'),
    html.Hr(),
    html.Div([
        html.H2('Parameters'),
        html.Div(dcc.Input(id='person', type='text', placeholder="person")),
        html.Button('Get parameters', id='submit-parameters', n_clicks=0),
        html.Div(id='container-parameters')
    ]),
    html.Hr(),
    html.Div([
        html.H2('Create table'),
        html.Div([
            dcc.Input(id='table-type', type='text', placeholder="table type"),
            dcc.Input(id='number-rows', type='number', placeholder="number of rows")
        ]),
        html.Button('Create new table', id='submit-create-table', n_clicks=0),
        html.Button('Store table', id='submit-store-table', n_clicks=0),
        html.Div(id='container-table'),
        html.Div(id="container-hidden", style={"display": "none"})
    ])
])
# html.Button('Fetch table', id='submit-fetch-table', n_clicks=0),

@callback(
    Output('container-parameters', 'children'),
    Input('submit-parameters', "n_clicks"),
    State('person', 'value'),
    prevent_initial_call=True
)
def update_parameters(n_clicks, value):
    # TODO Move to other module?
    config.person = value
    return 'Person: "{}" '.format(value)

@callback(
    Output('container-table', 'children'),
    Input('submit-create-table', "n_clicks"),
    State('table-type', 'value'),
    State('number-rows', 'value'),
    prevent_initial_call=True
)
def create_table(n_clicks, table_type, n_rows):
    config.table_edit = TableOperations.create_table(TableType[table_type], config.person, n_rows)
    return html.Div([
        dash_table.DataTable(
            id='table',
            data=config.table_edit["df"].table.to_dict('records'),
            columns=[{"name": i, "id": i} for i in config.table_edit["df"].table.columns],
            editable=True
        )
    ])

# @callback(
#     Output('container-table', 'children', allow_duplicate=True),
#     Input('submit-fetch-table', "n_clicks"),
#     State('table-type', 'value'),
#     prevent_initial_call=True
# )
# def fetch_table(n_clicks, table_type):
#     config.table_edit["type"] = TableType[table_type]
#     config.table_edit["name"] = config.person + "_" + config.table_edit["type"].name
#     if config.table_edit["mysql"] is None:
#         config.table_edit["mysql"] = MySQL.init_table(
#             config.mysql["engine"],
#             config.mysql["metadata"],
#             config.table_edit["name"]
#         )
#     df = MySQL.table_fetch(config.mysql["conn"], config.table_edit["mysql"])
#     config.table_edit["df"] = DataTableFactory.create_table(config.table_edit["type"], df)
#     return html.Div([
#         dash_table.DataTable(
#             id='table',
#             data=config.table_edit["df"].table.to_dict('records'),
#             columns=[{"name": i, "id": i} for i in config.table_edit["df"].table.columns],
#             editable=True
#         )
#     ])

@callback(
    Output('container-hidden', 'children'),
    Input('table', 'data'),
    Input('table', 'columns'),
    prevent_initial_call=True)
def edit_table(rows, columns):
    # TODO sqlalchemy also be updated?
    config.table_edit["df"].table = pd.DataFrame(rows, columns=[c['name'] for c in columns])
    return ""

@callback(
    Output('container-hidden', 'children', allow_duplicate=True),
    Input('submit-store-table', "n_clicks"),
    prevent_initial_call=True)
def store_table(n_clicks):
    MySQL.table_insert(
        config.mysql["conn"],
        config.table_edit["mysql"],
        config.table_edit["df"].table
    )
