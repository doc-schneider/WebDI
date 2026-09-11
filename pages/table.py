import dash
from dash import html, Input, Output, ctx, callback, dcc
from flask import session

from Views.Table import TableViewer
from Views.View_Factory import ViewFactory
from DataStructures.TableTypes import TableType
from Initialize.Formats import box_style
import config

'''
- xyz
'''

def create_Table():
    TableView = init_Table(session['table_content'])
    boxes_dct = TableView.view()
    n_rows = boxes_dct["N_DIM"]
    return html.Div(
        [
            html.Div(
                [
                    html.Div("Von:", style=box_style),
                    html.Div("Bis:", style=box_style),
                    html.Div("", style=box_style),
                    html.Div("", style=box_style)
                ], style={'display': 'flex', 'flexDirection': 'row'}
            )
        ] +
        [
            html.Div(
                ViewFactory.additional_items(
                    boxes_dct, r, 'DATE_FROM', box_style
                ) + ViewFactory.additional_items(boxes_dct, r, 'DATE_TO', box_style) + [
                    html.Div(boxes_dct["TEXT"][r], style=box_style)
                ] + ViewFactory.additional_items(
                    boxes_dct, r, 'TEXT_ADDITIONAL', box_style
                ),
                style={'display': 'flex', 'flexDirection': 'row'},
                id={"type": "box-table", "index": r}
            ) for r in range(n_rows)
        ],
        style={"display": "flex", "flex-direction": "column"}
    )

dash.register_page(__name__)

def layout():
    if "initialized" not in session:
        return html.Div([
            html.Br(),
            html.Br(),
        ])
    else:
        return html.Div([
            html.Br(),
            html.Br(),
            create_Table()
        ])

def init_Table(table_content):
    data_table = ViewFactory.filter_table(
        config.table[TableType[table_content]]["data_table"],
        session
    )
    return TableViewer(
        data_table
    )
