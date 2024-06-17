import dash
from dash import dcc, html, Input, Output, State, callback, dash_table
import pandas as pd

from DataStructures.Data import DataTable
from Views.Content import ContentViewer
import config


dash.register_page(__name__)

layout = html.Div([
    html.H1('Content'),
    html.Hr(),
    html.Div(id='content')
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
        content_dct = config.ContentView.view()
        return html.Div([
            html.Img(src="data:image/jpeg;base64," + content_dct["IMAGE"][0], width="100%"),
            html.Div(content_dct["DESCRIPTION"][0])
        ])

def init_Content(ix):
    config.ContentView = ContentViewer(
        DataTable(
            config.TimelineView.datatable.table.iloc[[ix]],
            config.TimelineView.datatable.table_type
        )
    )

