import dash
import pandas as pd
from dash import html, Input, Output, callback, ctx, dcc, ALL
from flask import session

from Views.Timeline import TimelineViewer
from DataStructures.TableTypes import TableType
import config

# Definition of layout on page
n_rows_default = 10  # TODO Get from session

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
    boxes_dct["grid_location"] = pd.Series([None] * n_cols)
    for i in range(n_cols):
        if boxes_dct["ID"][i]:
            boxes_dct["grid_location"][i] = int(
                100 * (boxes_dct["DATE_TIME"][i] - boxes_dct["TIME_GRID"][i].left) / boxes_dct["TIME_GRID"][i].length
            )

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
           ] + [
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
                [
                    html.Div(boxes_dct["TEXT"][i]),
                    html.Div("Datum: " + boxes_dct["DATE_TIME"][i].strftime('%Y-%m-%d %X'))
                ] + additional_items(boxes_dct, i, 'TEXT_ADDITIONAL'),
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

def additional_items(boxes_dct, i, item):
    if item in boxes_dct.keys():
        return [
            txt_add[i] for _, txt_add in boxes_dct[item].items()
        ]
    else:
        return []

def init_Timeline(timeline_content, timeline_view):
    data_table = config.table[TableType[timeline_content]]["data_table"]
    return TimelineViewer(
        data_table,
        timeline_view,
    )


# Click one box for redirect to photo page
# @callback(
#     Output("url-redirect", "href"),
#     Input({"type": "box-timeline", "index": ALL}, "n_clicks"),
#     prevent_initial_call=True
# )
# def click_box(n_clicks_list_box):
#     if any(c is not None for c in n_clicks_list_box):
#         ix = ctx.triggered_id["index"]
#         session["content_content"] = TableType.ALBUM.name
#         #AlbumView = init_Album(session['ALBUM'], session["album_view"])
#         #session['content_view']["ID_PHOTO"] = AlbumView.datatable_show.table.loc[ix, "ID_PHOTO"]
#         return "/content"



# # Global definitions
# box_width = 10.0      # Percentage to 100%
# box_height = 50.0
# box_distance = 5.0

# layout = html.Div([
#     html.H1('Timeline'),
#     svg.Svg(
#         width="100%",
#         height="500",
#         id='container-svg'
#     ),
#
# ])

# def create_svg():
#     # Initialize at first call
#     if not hasattr(config, 'TimelineView'):
#         init_Timeline()
#     timeline_dct = config.TimelineView.view()
#
#     # Convert to percentages
#     time_grid = 100 / timeline_dct["N_GRID"] * np.arange(timeline_dct["N_GRID"])   # Relative to 100%
#     time_grid_str = [
#         timeline_dct["TIME_GRID"][i].strftime('%Y-%m-%d %H:%M')
#         for i in range(timeline_dct["N_GRID"])
#     ]
#
#     # Content boxes (that can be shown)
#     ix_display, x_display = time_boxes(
#         timeline_dct["TIME_INTERVAL"],
#         timeline_dct["DATE_TIME"]
#     )
#     content_display = []
#     if config.table["table_type"].name == "PHOTO":
#         for ix in ix_display:
#             content_display.append(
#                 timeline_dct["IMAGE"][ix]
#             )
#
#     return svg.G(
#         fill='blue',
#         children=[
#             svg.Rect(x="0", y="0%", width="100%", height="0.5%", fill="black"),
#             svg.Rect(x="0", y="99.5%", width="100%", height="0.5%", fill="black"),
#         ] + [
#             svg.Rect(x="{}%".format(x), y="98%", width="0.25%", height="2%", fill="black") for x in time_grid
#         ] + [
#             svg.Text(
#                 time_grid_str[i],
#                 x="{}%".format(time_grid[i]),
#                 y="97.5%", stroke="black") for i in range(timeline_dct["N_GRID"])
#         ] + [
#             svg.Line(
#                 x1="{}%".format(x),
#                 y1="100%",
#                 x2="{}%".format(x),
#                 y2="80%",
#                 stroke="black",
#                 strokeWidth="2"
#             ) for x in x_display
#         ] + [
#             svg.Rect(
#                 x="{}%".format(x_display[i]),
#                 y="{}%".format(80-box_height),
#                 width="{}%".format(box_width),
#                 height="{}%".format(box_height),
#                 stroke="black",
#                 strokeWidth="2",
#                 fillOpacity="20%"
#             ) for i in range(len(x_display))
#         ] + [
#             dcc.Link(
#                 svg.ForeignObject(
#                     children=[
#                         html.Img(
#                             src="data:image/jpeg;base64," + content_display[i],
#                             width="100%"
#                         )
#                     ],
#                     x="{}%".format(x_display[i]),
#                     y="{}%".format(80-box_height),
#                     width="{}%".format(box_width),
#                     height="{}%".format(box_height),
#                     id={"type": "box", "index": ix_display[i]},
#                     n_clicks=0
#                 ),
#                 href=dash.page_registry["pages.content"]["relative_path"],
#                 refresh=True
#             ) for i in range(len(ix_display))
#         ]
#     )
#
# def init_Timeline():
#     config.TimelineView = TimelineViewer(config.table["data_table"])
#
# def time_boxes(time_interval, boxes_time):
#     # Boxers that can be shown without overlap
#     # TODO Round
#     if len(boxes_time) > 0:
#         x_all = [
#             100 * (pd.Interval(time_interval.left, r, closed='left').length / time_interval.length) for r in boxes_time
#         ]
#         ix = [0]  # Indices
#         x = [x_all[0]]  # x coordinates
#         for i in range(1, len(x_all)):
#             if x_all[i] - x_all[i-1] >= box_width + box_distance:
#                 ix.append(i)
#                 x.append(x_all[i])
#     else:
#         ix = []
#         x = []
#     return ix, x

