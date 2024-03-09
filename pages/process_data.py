import dash
from dash import dcc, html, Input, Output, State, callback, dash_table
import pandas as pd

import config


dash.register_page(__name__)

layout = html.Div([
    html.H1('Data processing page'),
    html.Hr(),
    html.Div([
        html.H2('Parameters'),
        html.Div(dcc.Input(id='person', type='text', placeholder="person")),
        html.Button('Get parameters', id='submit-parameters', n_clicks=0),
        html.Div(id='container-parameters')
    ]),
])

