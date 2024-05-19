import dash
from dash import dcc, html, Input, Output, State, callback, dash_table
import pandas as pd

from Views.Content import ContentViewer
import config


dash.register_page(__name__)

layout = html.Div([
    html.H1('Content'),
    html.Hr(),
    html.Div([
        html.H2(id="title"),
        html.Div(id='content')
    ]),
])

@callback(
    Output('content', 'children'),
    Input('store', 'data')
)
def update_content(data):
    if data is None:
        return None
    else:
        init_Content(data['index'])  # Todo Actually only necessary if content has changed
        return f"Data received: {data['index']}"

def init_Content(ix):
    config.ContentView = ContentViewer(
        config.TimelineView.datatable.table.iloc[[ix]]
    )

