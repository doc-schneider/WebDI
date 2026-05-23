import dash
from dash import dcc, html, callback, Input, Output
from flask import session

from DataStructures.TableTypes import TableType
from Initialize.Formats import button_style

# timeline_contents = [TableType.ALBUM.name, TableType.MESSAGE.name, TableType.NOTE.name]


dash.register_page(__name__, path='/')

layout = html.Div([
    html.H1('Homepage'),
    html.Br(),
    html.Div(
        [
            html.Button('Fotoalben', id={"type": "button-home", "index": TableType.ALBUM.name}, n_clicks=0, style=button_style),
            html.Button('Filme', id={"type": "button-home", "index": TableType.FILM.name}, n_clicks=0, style=button_style),
            html.Button('SMS', id={"type": "button-home", "index": TableType.MESSAGE.name}, n_clicks=0, style=button_style),
            html.Button('Notizen', id={"type": "button-home", "index": TableType.NOTE.name}, n_clicks=0, style=button_style),
        ],
        style={
            "display": "flex",
            "gap": "10px",          # Abstand zwischen Buttons
            "alignItems": "center"
        }
    ),
])
    # html.Br(),
    # html.Br(),
    # html.Label("Timeline Inhalt:"),
    # dcc.Dropdown(
    #     id="home-dropdown",
    #     options=[{"label": "Wählen", "value": "empty"}] + [{"label": x, "value": x} for x in timeline_contents],
    #     value="empty",
    #     clearable=False,
    #     style={"width": "300px"},
    # ),
    # html.Div(id="home-dummy", style={"display": "none"})

# @callback(
#     Output("home-dummy", "children"),
#     Input("home-dropdown", "value"),
#     prevent_initial_call=True
# )
# def update_timeline_content(value):
#     session['timeline_content'] = value
#     return ""

