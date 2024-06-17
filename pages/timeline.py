import dash
from dash import html, Input, Output, callback, ctx, ALL, dcc, State
import dash_svg as svg
import pandas as pd
import numpy as np

from Views.Timeline import TimelineViewer
import config

'''
- xyz
'''

# Global definitions
box_width = 10.0      # Percentage to 100%
box_height = 50.0
box_distance = 5.0


dash.register_page(__name__)

layout = html.Div([
    html.H1('Timeline'),
    svg.Svg(
        width="100%",
        height="500",
        id='container-svg'
    ),
    html.Button('earlier', id='earlier', n_clicks=0),
    html.Button('later', id='later', n_clicks=0),
    html.Button('zoom in', id='zoom-in', n_clicks=0),
    html.Button('zoom out', id='zoom-out', n_clicks=0)
])

@callback(
    Output(component_id='container-svg', component_property='children'),
    Input('earlier', "n_clicks"),
    Input('later', "n_clicks"),
    Input('zoom-in', "n_clicks"),
    Input('zoom-out', "n_clicks")
)
def update_timeline(b1, b2, b3, b4):
    if ctx.triggered_id == "earlier":
        config.TimelineView.earlier(config.table["datatable"])
    elif ctx.triggered_id == "later":
        config.TimelineView.later(config.table["datatable"])
    elif ctx.triggered_id == "zoom-in":
        config.TimelineView.zoom_in(config.table["datatable"])
    elif ctx.triggered_id == "zoom-out":
        config.TimelineView.zoom_out(config.table["datatable"])
    else:
        pass  # None. Initial or refresh
    return create_svg()

def create_svg():
    # Initialize at first call
    if not hasattr(config, 'TimelineView'):
        init_Timeline()
    timeline_dct = config.TimelineView.view()

    # Convert to percentages
    time_grid = 100 / timeline_dct["N_GRID"] * np.arange(timeline_dct["N_GRID"])   # Relative to 100%
    time_grid_str = [
        timeline_dct["TIME_GRID"][i].strftime('%Y-%m-%d %H:%M')
        for i in range(timeline_dct["N_GRID"])
    ]

    # Content boxes (that can be shown)
    ix_display, x_display = time_boxes(
        timeline_dct["TIME_INTERVAL"],
        timeline_dct["DATE_TIME"]
    )
    content_display = []
    if config.table["table_type"].name == "PHOTO":
        for ix in ix_display:
            content_display.append(
                timeline_dct["IMAGE"][ix]
            )

    return svg.G(
        fill='blue',
        children=[
            svg.Rect(x="0", y="0%", width="100%", height="0.5%", fill="black"),
            svg.Rect(x="0", y="99.5%", width="100%", height="0.5%", fill="black"),
        ] + [
            svg.Rect(x="{}%".format(x), y="98%", width="0.25%", height="2%", fill="black") for x in time_grid
        ] + [
            svg.Text(
                time_grid_str[i],
                x="{}%".format(time_grid[i]),
                y="97.5%", stroke="black") for i in range(timeline_dct["N_GRID"])
        ] + [
            svg.Line(
                x1="{}%".format(x),
                y1="100%",
                x2="{}%".format(x),
                y2="80%",
                stroke="black",
                strokeWidth="2"
            ) for x in x_display
        ] + [
            svg.Rect(
                x="{}%".format(x_display[i]),
                y="{}%".format(80-box_height),
                width="{}%".format(box_width),
                height="{}%".format(box_height),
                stroke="black",
                strokeWidth="2",
                fillOpacity="20%"
            ) for i in range(len(x_display))
        ] + [
            dcc.Link(
                svg.ForeignObject(
                    children=[
                        html.Img(
                            src="data:image/jpeg;base64," + content_display[i],
                            width="100%"
                        )
                    ],
                    x="{}%".format(x_display[i]),
                    y="{}%".format(80-box_height),
                    width="{}%".format(box_width),
                    height="{}%".format(box_height),
                    id={"type": "box", "index": ix_display[i]},
                    n_clicks=0
                ),
                href=dash.page_registry["pages.content"]["relative_path"],
                refresh=True
            ) for i in range(len(ix_display))
        ]
    )

def init_Timeline():
    config.TimelineView = TimelineViewer(config.table["data_table"])

def time_boxes(time_interval, boxes_time):
    # Boxers that can be shown without overlap
    # TODO Round
    if len(boxes_time) > 0:
        x_all = [
            100 * (pd.Interval(time_interval.left, r, closed='left').length / time_interval.length) for r in boxes_time
        ]
        ix = [0]  # Indices
        x = [x_all[0]]  # x coordinates
        for i in range(1, len(x_all)):
            if x_all[i] - x_all[i-1] >= box_width + box_distance:
                ix.append(i)
                x.append(x_all[i])
    else:
        ix = []
        x = []
    return ix, x

# TODO:
#  - Why is this callback triggered: 1) Starting the app, 2) Building up this page, 3) Multiple times when clicking just one box
#  - Why is this working even without a box id at initial call?
#  - Why is the store data not updated at very first click? Still the case?
@callback(
    Output('store', 'data'),
    Input({"type": "box", "index": ALL}, "n_clicks"),
    Input('store', 'data')
)
def click_box(values, data):
    # Need to do all the extra stuff to no loose store data by empty calls
    if ctx.triggered_id and (ctx.triggered_id != "store"):   # TODO: Why can this be store?
        ix = ctx.triggered_id["index"]
        if any(values):
            return {'index': ix}
        else:
            return data
    else:
        return data

