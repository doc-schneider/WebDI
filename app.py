from dash import Dash, dcc, callback, html, Input, Output, State, ctx, ALL
from sqlalchemy import create_engine, MetaData
import mysql.connector

from DataStructures.Data import DataTable
from DataStructures.TableTypes import TableType
from Page.album import update_album, init_Album
from Page.collection import init_Collection
import config


# MySQL
db_connection_str = 'mysql+mysqlconnector://root:Moppel3!@localhost/lives'
db_engine = create_engine(db_connection_str)
db_conn = db_engine.connect()
metadata = MetaData()
metadata.reflect(bind=db_engine)
config.mysql = {
    "engine": db_engine,
    "conn": db_conn,
    "metadata": metadata,
}
# Simple connector
db_connector = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Moppel3!",
    database="lives",
)
db_cursor = db_connector.cursor()
config.mysql["connector"] = db_connector
config.mysql["cursor"] = db_cursor

# Tables
config.table = {
    TableType.ALBUM: {
        "mysql_name": "albums",
        "mysql_table": None,
        "data_table": None
    },
    TableType.PHOTO: {
        "mysql_name": "photos",
        "mysql_table": None,
        "data_table": None
    },
    TableType.NOTE: {
        "mysql_name": "notes",
        "mysql_table": None,
        "data_table": None
    },
    TableType.NOTEBOOK: {
        "mysql_name": "notebooks",
        "mysql_table": None,
        "data_table": None
    },
    TableType.DOCUMENT: {
        "mysql_name": "documents",
        "mysql_table": None,
        "data_table": None
    },
    TableType.DOCUMENT_COLLECTION: {
        "mysql_name": "document_collections",
        "mysql_table": None,
        "data_table": None
    },
    TableType.TAG: {
        "mysql_name": "tags",
        "mysql_table": None,
        "data_table": None
    },
    TableType.EVENT: {
        "mysql_name": "events",
        "mysql_table": None,
        "data_table": None
    },
}
for key in config.table.keys():
    config.table[key]["data_table"] = DataTable.fetch_table(
        key,
        config.table[key]["mysql_name"]
    )
config.collection_types = [TableType.ALBUM, TableType.NOTE, TableType.NOTEBOOK]  #TODO What was that for?

dash_app = Dash(__name__, suppress_callback_exceptions=True)

CollectionView = init_Collection(
    config.table[TableType.ALBUM]["data_table"]
)
collection_dct = CollectionView.view()
title = collection_dct["PHOTO_ALBUM"]["value"]
n_elements = CollectionView.collection["N_ELEMENTS"]
layout_collection = html.Div([
    html.Br(),
    html.Br(),
    html.Div([
        html.Div([
            html.Div(
                title[i],
                style={'backgroundColor': '#aaffaa', 'flex': 1, 'padding': '10px', 'border': '1px solid black'},
                id={"type": "item_collection", "index": i}
            ),
        ], style={'display': 'flex', 'flexDirection': 'row'}
        ) for i in range(n_elements)
    ]),
    html.Br(),
    html.Br(),
])

layout_album = html.Div([
    html.Br(),
    html.Div([
        html.Button('früher', id='earlier', n_clicks=0),
        html.Button('später', id='later', n_clicks=0),
    ], style={'display': 'flex', 'justify-content': 'center'}
    ),
    html.Div(id="album"),
    html.Br(),
    html.Br(),
    html.Div(
        dcc.Slider(
            min=1,
            max=240,
            value=1,
            step=1,
            id='album-slider'
        )
    ),
])

dash_app.layout = html.Div([
    html.Br(),
    html.Br(),
    html.Br(),
    html.Div(id='page-content', children=layout_album),
    dcc.Store(
        id='store', storage_type='session', data={
            "type": TableType.ALBUM.name,
            "album": {"ID_ALBUM": 6},
            "album_view": {"ID_PHOTO": [None]}
        }
    ),
])

# @callback(
#     Output('page-content', 'children'),
#     Input('id-dropdown', 'value'),
# )
# def display_page(selected_value):
#     if selected_value == "albums":
#         return layout_collection
#     elif selected_value == "photos":
#         print("!")
#         return layout_album

# @callback(
#     Output('store', 'data'),
#     Input({"type": "item_collection", "index": ALL}, "n_clicks"),
#     State('store', 'data'),
#     prevent_initial_call=True,
#     allow_duplicate=True
# )
# def click_box(box_click, store_data):
#     print(ctx.triggered_id)
#     print(box_click)
#     return store_data

@callback(
    Output('album', 'children'),
    Output('album-slider', 'max'),
    Output('album-slider', 'value'),
    Output('album-slider', 'marks'),
    Output('store', 'data'),
    Input('earlier', "n_clicks"),
    Input('later', "n_clicks"),
    Input('album-slider', 'value'),
    State('store', 'data'),
)
def click_button_album(b1, b2, slider_value, store_data):
    print(store_data["album_view"])
    AlbumView = init_Album(store_data["album"], store_data["album_view"])
    if ctx.triggered_id == "earlier" and b1 > 0:  # TODO ctx gives a wrong value for no click (earlier)
        AlbumView.earlier()
    elif ctx.triggered_id == "later":
        AlbumView.later()
    elif ctx.triggered_id == "album-slider":
        AlbumView.jump(slider_value - 1)
    else:
        pass  # None. Initial or refresh
    store_data["album_view"] = {"ID_PHOTO": list(AlbumView.ix_show)}
    print(store_data["album_view"])
    return update_album(AlbumView) + (store_data,)

if __name__ == '__main__':
    dash_app.run(host='192.168.0.225', port=5000, debug=True)  # (debug=True)   (host='192.168.0.225', port=5000, debug=True)



