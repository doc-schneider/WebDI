import dash
from dash import dcc, html, callback, Input, Output
from flask import session


dash.register_page(__name__)

layout = html.Div([
    html.H1('Fotoalbum')
])
