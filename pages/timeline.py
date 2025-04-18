import dash
import pandas as pd
from dash import html, Input, Output, State, callback, ctx, dcc, ALL, MATCH
import datetime as dtm
from flask import session

from DataStructures.TableTypes import TableType
from DataOperations.Photo import allow_formats_image, allow_formats_video
from Views.Timeline import TimelineViewer
import config

'''
- xyz
'''


dash.register_page(__name__)

layout = html.Div([
    html.Br(),
    html.Div([
        html.Button('earlier', id='earlier', n_clicks=0),
        html.Button('later', id='later', n_clicks=0),
        html.Button('zoom in', id='zoom-in', n_clicks=0),
        html.Button('zoom out', id='zoom-out', n_clicks=0)
    ], style={'display': 'flex', 'justify-content': 'center'}
    ),
    html.Div(id="timeline"),
    html.Br(),
])

@callback(
    Output('timeline', 'children'),
    Input('earlier', "n_clicks"),
    Input('later', "n_clicks"),
    Input('zoom-in', "n_clicks"),
    Input('zoom-out', "n_clicks"),
)
def click_timeline(be, bl, bi, bo):
    TimelineView = init_Timeline(session['message_collection'], session["message_view"])
    if ctx.triggered_id == "earlier":
        TimelineView.earlier()
    elif ctx.triggered_id == "later":
        TimelineView.later()
    elif ctx.triggered_id == "zoom-in":
        TimelineView.zoom_in()
    elif ctx.triggered_id == "zoom-out":
        TimelineView.zoom_out()
    else:
        pass  # None. Initial or refresh
    session['message_view'] = {
        "GRANULARITY": TimelineView.granularity,
        "DATETIME_START": TimelineView.time_grid[0].left
    }
    return update_timeline(TimelineView)

def update_timeline(TimelineView):
    boxes_dct = TimelineView.view()
    n_boxes = boxes_dct["N_BOXES"]
    time_grid = boxes_dct["TIME_GRID"]
    return [
        html.Div([
            html.Div(
                boxes_dct["TEXT"]["value"][i],
                style={'flex': 1, 'padding': '10px', 'border': '1px solid black'}
            ) for i in range(n_boxes)
        ], style={'display': 'flex', 'flexDirection': 'row'})
    ]

def init_Timeline(message_collection, message_view):
    return TimelineViewer(
        config.table[TableType.MESSAGE]["data_table"],
        message_collection,
        message_view
    )
