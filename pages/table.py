import dash
from dash import html, Input, Output, ctx, callback, dcc
from flask import session

from Views.Table import TableViewer
from Views.View_Factory import ViewFactory
from DataStructures.TableTypes import TableType
import config

'''
- xyz
'''


def create_Table():
    TableView = init_Table(session['table_content'])
    boxes_dct = TableView.view()
    n_rows = boxes_dct["N_DIM"]
    return html.Div([
        html.Div(
            [
                html.Div(boxes_dct["TEXT"][r])
            ] + ViewFactory.additional_items(boxes_dct, r, 'TEXT_ADDITIONAL'),
            style={'flex': 1, 'padding': '5px',
                   'borderLeft': '1px solid black',
                    'borderRight': '1px solid black',
                    'borderTop': '1px solid black',
                    'borderBottom': '1px solid black',
                    "background-color": "gainsboro"
                   },
            id={"type": "box-table", "index": r}
        ) for r in range(n_rows)
    ], style={"display": "flex", "flex-direction": "column", "gap": "5px"})

dash.register_page(__name__)

def layout():
    return html.Div([
        html.Br(),
        html.Br(),
        create_Table()
    ])

def init_Table(table_content):
    data_table = config.table[TableType[table_content]]["data_table"]
    return TableViewer(
        data_table
    )
