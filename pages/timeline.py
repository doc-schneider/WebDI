import dash
from dash import html, Input, Output, callback, dash_table, dcc
import dash_svg as svg

import config

'''
- Shows a Table view of the Topic Table
- A Topic can be clicked to get to the Sub-Topics
'''

dash.register_page(__name__)

layout = html.Div([
    html.H1('Timeline'),
    svg.Svg(
        width="100%",
        height="500",
        children=svg.G(
            fill='blue',
            children=[
                svg.Rect(x="0", y="0%", width="100%", height="1%", fill="black"),
                svg.Rect(x="50%", y="50%", width="10%", height="10%", rx="2%", ry="2%", fill="red", stroke="black", opacity="0.5"),
                svg.Rect(x="0", y="99%", width="100%", height="1%", fill="black"),
            ]
        )
    ),
    dcc.Input(id='input-1-state', type='text', value='Montréal'),
    dcc.Input(id='input-2-state', type='text', value='Canada'),
    html.Button(id='submit-button-state', n_clicks=0, children='Submit'),
])

