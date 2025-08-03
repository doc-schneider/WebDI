import dash
from dash import html, Input, Output, State, callback, ctx, dcc, ALL, MATCH
from flask import session

from DataStructures.TableTypes import TableType, table_definitions
from DataOperations.Photo import allow_formats_image, allow_formats_video
from Views.Timeline import TimelineViewer
import config

# Definition of layout on page
n_rows_default = 10

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
        html.Button('zoom out', id='zoom-out', n_clicks=0),
        html.Label("Max number of rows:"),
        dcc.Input(
            id='number-rows',
            type='number',
            value=n_rows_default,
        ),
    ], style={'display': 'flex', 'justify-content': 'center'}
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
    TimelineView = init_Timeline(
        session['timeline_content'],
        session["timeline_view"],
        n_rows
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
        "DATETIME_START": TimelineView.time_grid[0].left
    }
    return update_timeline(TimelineView)

def update_timeline(TimelineView):
    boxes_dct = TimelineView.view()
    n_rows, n_cols = boxes_dct["N_DIM"]
    return [
               html.Div([
                   html.Div(
                       boxes_dct["TIME_GRID"][i].strftime('%Y-%m-%d %X'),
                       style={'flex': 1, 'padding': '10px',
                              'borderLeft': '2px solid black',
                              'borderRight': '2px solid black',
                              'borderTop': '1px solid blue',
                              'borderBottom': '1px solid blue',
                              }
                   ) for i in range(n_cols)
               ], style={'display': 'flex', 'flexDirection': 'row'})
           ] + [
        html.Div([
            html.Div(
                [
                    html.Div(boxes_dct["TEXT"][i]),
                    media_type_box(
                        boxes_dct["FILE_FORMAT"][i],
                        boxes_dct["IMAGE"][i],
                        i,
                    ),
                    html.Div("Datum: " + boxes_dct["DATE_TIME"][i].strftime('%Y-%m-%d %X'))
                ] + additional_items(boxes_dct, i, 'TEXT_ADDITIONAL'),
                style={'flex': 1, 'padding': '10px',
                       'borderLeft': '2px solid black',
                       'borderRight': '2px solid black',
                       'borderTop': '1px solid black',
                       'borderBottom': '1px solid black',
                       }
            ) if boxes_dct["ID"][i] else html.Div(
                [],
                style={'flex': 1, 'padding': '10px',
                       'borderLeft': '2px solid black',
                       'borderRight': '2px solid black',
                       'borderTop': '1px solid black',
                       'borderBottom': '1px solid black',
                       }
            ) for i in range(r * n_cols, (r + 1) * n_cols)
        ], style={'display': 'flex', 'flexDirection': 'row'}) for r in range(n_rows)
    ]

# TODO Into ViewFactory
def media_type_box(media_type, content_display, i):
    if media_type in allow_formats_image:
        return html.Img(
            src="data:image/jpeg;base64," + content_display,
            width="100%",
            id={"type": "box", "index": i}
        )
    elif media_type in allow_formats_video:
        return html.Video(
            src=content_display,
            controls=True,
            width="100%",
            id={"type": "box", "index": i}
        )
    else:
        return html.Div()

def additional_items(boxes_dct, i, item):
    if item in boxes_dct.keys():
        return [
            txt_add[i] for _, txt_add in boxes_dct[item].items()
        ]
    else:
        return []

def init_Timeline(timeline_content, timeline_view, n_rows):
    # TODO Move to Timeline (?)
    data_table = config.table[TableType[timeline_content]]["data_table"]
    parent_table_type = table_definitions[TableType[timeline_content]]["ParentTableType"]
    parent_id = session[parent_table_type.name][
        table_definitions[TableType[parent_table_type.name]]["PrimaryKey"]
    ]
    return TimelineViewer(
        data_table.match_foreignkey(parent_id),
        timeline_view,
        n_rows
    )
