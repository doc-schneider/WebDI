import dash
from dash import dcc, html, callback, Input, Output, ALL, ctx
from flask import session

from DataStructures.TableTypes import TableType
from Initialize.Formats import button_style
import config

# TODO To be determined at start
dropdown_contents = {
    TableType.MESSAGE.name: ["SMS", "WhatsApp"]
}
ITEM_WIDTH = "180px"


dash.register_page(__name__, path='/')

layout = html.Div([
    html.H1('Homepage'),
    html.Br(),
    html.Div(
        [
            html.Button('Fotoalben', id={"type": "button-home", "index": TableType.ALBUM.name}, n_clicks=0, style={**button_style, "width": ITEM_WIDTH}),
            html.Button('Filme', id={"type": "button-home", "index": TableType.FILM.name}, n_clicks=0, style={**button_style, "width": ITEM_WIDTH}),
            html.Button(
                'Nachrichten',
                id={"type": "button-home", "index": TableType.MESSAGE.name},
                n_clicks=0,
                style={**button_style, "width": ITEM_WIDTH}
            ),
            html.Button('Notizen', id={"type": "button-home", "index": TableType.NOTE.name}, n_clicks=0, style={**button_style, "width": ITEM_WIDTH}),
        ],
        style={
            "display": "flex",
            "gap": "10px",          # Abstand zwischen Buttons
            "alignItems": "center"
        }
    ),
    html.Div(
        [
            dcc.Dropdown(
                id={"type": "dropdown-home", "index": TableType.ALBUM.name},
                options=[],
                placeholder="Filter...",
                style={"width": ITEM_WIDTH},
            ),
            dcc.Dropdown(
                id={"type": "dropdown-home", "index": TableType.FILM.name},
                options=[],
                placeholder="Filter...",
                style={"width": ITEM_WIDTH},
            ),
            dcc.Dropdown(
                id={"type": "dropdown-home", "index": TableType.MESSAGE.name},
                options=[{"label": x, "value": x} for x in dropdown_contents[TableType.MESSAGE.name]],
                placeholder="Typ",
                style={"width": ITEM_WIDTH},
            ),
            dcc.Dropdown(
                id={"type": "dropdown-home", "index": TableType.NOTE.name},
                options=[],
                placeholder="Filter...",
                style={"width": ITEM_WIDTH},
            ),
        ],
        style={
            "display": "flex",
            "gap": "10px",
            "marginTop": "5px",
        },
    ),
    html.Div(id="home-dummy", style={"display": "none"})
])

@callback(
    Output("home-dummy", "children"),
    Input({"type": "dropdown-home", "index": ALL}, "value"),
    prevent_initial_call=True
)
def store_filters(values):

    trigger = ctx.triggered_id
    if trigger is not None:

        if trigger["index"] == TableType.MESSAGE.name:
            # TODO: This is just provisional
            ID_MESSAGE_COLLECTION = config.table[TableType[TableType.MESSAGE.name]]["data_table"].filter(
                {"MESSAGE_TYPE": values[2]}
            ).table["ID_MESSAGE_COLLECTION"].unique()[0]
            if values[2] == "SMS":
                session['MESSAGE_COLLECTION'] = {"ID_MESSAGE_COLLECTION": ID_MESSAGE_COLLECTION}
            elif values[2] == "WhatsApp":
                session['MESSAGE_COLLECTION'] = {"ID_MESSAGE_COLLECTION": ID_MESSAGE_COLLECTION}

    return ""
