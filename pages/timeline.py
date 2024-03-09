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
            id='container-svg'
        )
    ),
    dcc.Input(id='input-width', type='number', value=10),
])

@callback(
    Output(component_id='container-svg', component_property='children'),
    Input(component_id='input-width', component_property='value')
)
def create_svg(svg_width):
    return svg.G(
        fill='blue',
        children=[
            svg.Rect(x="0", y="0%", width="100%", height="1%", fill="black"),
            svg.Line(x1="50%", y1="99%", x2="50%", y2="50%", strokeWidth="2", stroke="blue"),
            svg.Rect(x="50%", y="50%", width=f"{svg_width}%", height="10%", fill="blue", stroke="black", opacity="0.5"),
            svg.Text("abc", x="55%", y="55%", stroke="black"),
            svg.Rect(x="0", y="99%", width="100%", height="1%", fill="black"),
        ]
    )
