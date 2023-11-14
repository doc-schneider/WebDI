#import pandas_datareader.data as web
#import pandas_datareader as pdr
#import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
#from dash.dependencies import Input, Output
import plotly.graph_objects as go


#start = datetime.datetime(2015,1,1)
#end = datetime.datetime(2018,2,8)
#symbol = 'WIKI/AAPL'  # or 'AAPL.US'
#df = web.DataReader(symbol, 'quandl', '2015-01-01', '2015-01-05')
#df = pdr.get_data_fred('GS10')

app = dash.Dash()

fig = go.Figure()
# Constants
img_width = 1600
img_height = 900
scale_factor = 0.5
# Add invisible scatter trace.
# This trace is added to help the autoresize logic work.
fig.add_trace(
    go.Scatter(
        x=[0, img_width * scale_factor],
        y=[0, img_height * scale_factor],
        mode="markers",
        marker_opacity=0
    )
)
# Configure axes
fig.update_xaxes(
    visible=False,
    range=[0, img_width * scale_factor]
)
fig.update_yaxes(
    visible=False,
    range=[0, img_height * scale_factor],
    # the scaleanchor attribute ensures that the aspect ratio stays constant
    scaleanchor="x"
)
# Add image
fig.add_layout_image(
    dict(
        x=0,
        sizex=img_width * scale_factor,
        y=img_height * scale_factor,
        sizey=img_height * scale_factor,
        xref="x",
        yref="y",
        opacity=1.0,
        layer="below",
        sizing="stretch",
        source="https://raw.githubusercontent.com/michaelbabyn/plot_data/master/bridge.jpg")
)
# Configure other layout
fig.update_layout(
    width=img_width * scale_factor,
    height=img_height * scale_factor,
    margin={"l": 0, "r": 0, "t": 0, "b": 0},
)

app.layout = html.Div(children=[
    dcc.Graph(
        id='test',
        figure=fig
    )
])

if __name__ == "__main__":
    app.run_server(debug=True)