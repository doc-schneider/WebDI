import dash
from dash import Dash, html, dcc


dash_app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True)
app = dash_app.server

dash_app.layout = html.Div([
    html.H1('Stefans Welt'),
    html.Div([
        html.Div(
            dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
        ) for page in dash.page_registry.values()
    ]),
    dash.page_container
])

if __name__ == '__main__':
    dash_app.run(debug=True)
