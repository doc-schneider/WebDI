import dash
import pandas as pd
from dash import html, Input, Output, callback, ctx, dcc
from flask import session

from Views.View_Factory import ViewFactory
from Views.Timeline import TimelineViewer
from DataStructures.TableTypes import TableType
from Initialize.Formats import button_style
import config

# Definition of layout on page
n_rows_default = 10  # TODO Get from session

'''
- xyz
'''

dash.register_page(__name__)

# TODO Editing of n_rows online can produce transient errors
layout = html.Div([
    html.Br(),
    html.Div([
        html.Button('früher', id='earlier', n_clicks=0, style=button_style),
        html.Button('später', id='later', n_clicks=0, style=button_style),
        html.Button('hineinzoomen', id='zoom-in', n_clicks=0, style=button_style),
        html.Button('herauszoomen', id='zoom-out', n_clicks=0, style=button_style),
        html.Label(html.B("Max Anzahl Reihen:")),
        dcc.Input(
            id='number-rows',
            type='number',
            value=n_rows_default,
        ),
    ], style={'display': 'flex', 'justify-content': 'center', "gap": "25px"}
    ),
    html.Br(),
    html.Div(id="timeline"),
])

@callback(
    Output('timeline', 'children'),
    Input('earlier', "n_clicks"),
    Input('later', "n_clicks"),
    Input('zoom-in', "n_clicks"),
    Input('zoom-out', "n_clicks"),
    Input('number-rows', 'value'),
)
def click_timeline(be, bl, bi, bo, n_rows):
    session['timeline_view']["n_rows"] = n_rows
    TimelineView = init_Timeline(
        session['timeline_content'],
        session["timeline_view"],
    )
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
    session['timeline_view'] = {
        "GRANULARITY": TimelineView.granularity,
        "DATETIME_START": TimelineView.time_grid[0].left,
        "n_rows": n_rows
    }
    return update_timeline(TimelineView)

def update_timeline(TimelineView):
    boxes_dct = TimelineView.view()
    n_rows, n_cols = boxes_dct["N_DIM"]

    # Find Start Time of first row items
    if n_rows > 0:  # Any entry at all?
        boxes_dct["grid_location"] = pd.Series([None] * n_cols)
        for i in range(n_cols):
            if boxes_dct["ID"][i]:
                boxes_dct["grid_location"][i] = int(
                    100 * (boxes_dct["DATE_TIME"][i] - boxes_dct["TIME_GRID"][i].left) / boxes_dct["TIME_GRID"][i].length
                )
        return layout_time_grid(
            boxes_dct, n_cols
        ) + [
            html.Div([
                html.Div(
                    style={
                        'flex': 1,
                        "position": "relative",
                        "height": "50px",
                        'padding': '5px',
                    },
                    children=[
                        html.Div(
                            style={
                                "position": "absolute",
                                "top": "0",
                                "left": "{}%".format(boxes_dct["grid_location"][i]),
                                "height": "100%",        # volle Höhe des Containers
                                "width": "2px",          # Liniendicke
                                "backgroundColor": "red"
                            }
                        )
                    ]
                ) if boxes_dct["ID"][i] else html.Div(
                    style={
                        'flex': 1,
                        "position": "relative",
                        "height": "50px",
                        'padding': '5px',
                    }
                ) for i in range(n_cols)
            ], style={'display': 'flex', 'flexDirection': 'row'})
        ] + [html.Div([
            html.Div([
                html.Div(
                    ViewFactory.media_type_box(
                        boxes_dct["FILE_FORMAT"][i],
                        boxes_dct["IMAGE"][i]
                    ) +
                    [
                        html.Div(boxes_dct["TEXT"][i]),
                        html.Div("Datum: " + boxes_dct["DATE_TIME"][i].strftime('%Y-%m-%d %X'))
                    ] + ViewFactory.additional_items(boxes_dct, i, 'TEXT_ADDITIONAL'),
                    style={'flex': 1, 'padding': '5px',
                           'borderLeft': '1px solid black',
                           'borderRight': '1px solid black',
                           'borderTop': '1px solid black',
                           'borderBottom': '1px solid black',
                           "background-color": "gainsboro"
                           },
                    id={"type": "box-timeline", "index": i}
                ) if boxes_dct["ID"][i] else html.Div(
                    [],
                    style={'flex': 1, 'padding': '5px',
                           'borderLeft': '1px solid black',
                           'borderRight': '1px solid black',
                           'borderTop': '1px solid black',
                           'borderBottom': '1px solid black',
                           }
                ) for i in range(r * n_cols, (r + 1) * n_cols)
            ], style={'display': 'flex', 'flexDirection': 'row', "gap": "5px"}) for r in range(n_rows)
        ], style={"display": "flex", "flex-direction": "column", "gap": "5px"})]
    else:
        return layout_time_grid(boxes_dct, n_cols)

def layout_time_grid(boxes_dct, n_cols):
    return [
        html.Div([
            html.Div(
                boxes_dct["TIME_GRID"][i].left.strftime('%Y-%m-%d %X'),
                style={'flex': 1,
                       'padding': '5px',
                       'borderLeft': '1px solid red',
                       'borderRight': '1px solid red',
                       'borderTop': '1px solid black',
                       'borderBottom': '1px solid red',
                       "background-color": "gainsboro"
                       }
            ) for i in range(n_cols)
        ], style={'display': 'flex', 'flexDirection': 'row'})
    ]

def init_Timeline(timeline_content, timeline_view):
    data_table = ViewFactory.filter_table(
        config.table[TableType[timeline_content]]["data_table"],
        session
    )
    return TimelineViewer(
        data_table,
        timeline_view,
    )
