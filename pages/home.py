import dash
from dash import html

import config


dash.register_page(__name__, path='/')

layout = html.Div([
    html.H1('This is our Home page'),
    html.Div('Content ..')
])

