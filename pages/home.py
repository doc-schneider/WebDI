import dash
from dash import html, dcc, callback, Input, Output

import config


dash.register_page(__name__, path='/')

layout = html.Div([
    html.H1('Homepage'),
])

