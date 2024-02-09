import dash
from dash import Dash, html, dcc
# from flask import Flask


# flask_server = Flask(__name__)
# app = Dash(__name__, server=flask_server, use_pages=True, suppress_callback_exceptions=True)
app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True)
app.layout = html.Div([
    html.H1('Multi-page app with Dash Pages'),
    html.Div([
        html.Div(
            dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
        ) for page in dash.page_registry.values()
    ]),
    dash.page_container
])
# server = app.server
if __name__ == '__main__':
    app.run(debug=True)
