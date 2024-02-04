import dash
from dash import html, Input, Output, callback, dash_table, dcc

import config

'''
- Shows a Table view of the Topic Table
- A Topic can be clicked to get to the Sub-Topics
'''

dash.register_page(__name__)

layout = html.Div([
    html.H1('Topics'),
    # html.Div([
    #     dcc.Location(id="url",  refresh="callback-nav"),
    #     dash_table.DataTable(
    #         id='table',
    #         data=config.table_view["df"].table.to_dict('records'),
    #         columns=[{"name": i, "id": i} for i in config.table_view["df"].table.columns],
    #     ),
    #     html.Div(id='container-info'),
    # ])
])

# TODO First reload table
#
# @callback(
#     Output("url", "href"),
#     Input('table', 'active_cell'),
#     prevent_initial_call=True
# )
# def table_click(active_cell):
#     return "/process-data"
#     # return str(active_cell) if active_cell else "Click the table"
