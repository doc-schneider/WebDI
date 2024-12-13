import dash
from dash import html, Input, Output, ctx, ALL, callback, dcc
from flask import session

from Views.Collection import CollectionViewer
from DataStructures.TableTypes import TableType
from SessionManager.ManageSessions import session_manager, show_session
import config

'''
- xyz
'''


dash.register_page(__name__)

layout = html.Div([
    html.Br(),
    html.Br(),
    dcc.Dropdown(
        id='id-dropdown',
        options=[
            {'label': v, 'value': v}
            for v in config.table[TableType.TAG]["data_table"].table["TAG"]
        ],
        value=config.table[TableType.TAG]["data_table"].table.loc[0, "TAG"],  # Default selected value
        clearable=False,
    ),
    html.Br(),
    html.Br(),
    html.Div(
        id="collection"
    ),
    html.Div(id='page-collection-dummy', style={'display': 'none'})
])

@callback(
    Output(component_id='collection', component_property='children'),
    Input('id-dropdown', 'value'),
    prevent_initial_call=False
)
def create_collection(selected_value):
    show_session("collection: start")

    # Init TAG for user if not yet done
    # session_manager()

    # Initial call or re-trigger?
    session_manager({"page": "collection"})
    # if not ctx.triggered_id:
    #     if session["page"] != "album":
    #         session_manager({"page": "album"})
    #     else:
    #         raise dash.exceptions.PreventUpdate

    # Drop choice
    session_manager({"collection": {"TAG": selected_value}})

    # TODO Distinction should be made in Collection. Here uniform data types
    if session["collection_type"] == TableType.ALBUM.name:
        CollectionView = init_Collection(
            config.table[TableType.ALBUM]["data_table"],
            session["collection"]
        )
        link_page = "pages.album"
    elif session["collection_type"] == TableType.NOTEBOOK.name:
        CollectionView = init_Collection(
            config.table[TableType.NOTEBOOK]["data_table"]
        )
        link_page = "pages.collection"
    elif session["collection_type"] == TableType.NOTE.name:
        CollectionView = init_Collection(
            config.table[TableType.NOTE]["data_table"]
        )
        link_page = "pages.content"
    collection_dct = CollectionView.view()
    title = collection_dct["TITLE"]
    description = collection_dct["TEXT"]
    date_time_0 = collection_dct["DATE_TIME_0"].dt.strftime('%Y-%m-%d %X')
    date_time_1 = collection_dct["DATE_TIME_1"].dt.strftime('%Y-%m-%d %X')
    n_elements = CollectionView.collection["N_ELEMENTS"]

    show_session("collection: end")

    return [
        html.Div([
            html.Div(
                date_time_0[i], style={'flex': 1, 'padding': '10px', 'border': '1px solid black'}
            ),
            html.Div(
                date_time_1[i], style={'flex': 1, 'padding': '10px', 'border': '1px solid black'}
            ),
            dcc.Link(
                html.Div(
                    title[i],
                    style={'backgroundColor': '#aaffaa', 'flex': 1, 'padding': '10px', 'border': '1px solid black'},
                    id={"type": "item", "index": i}
                ),
                href=dash.page_registry[link_page]["relative_path"], refresh=True
            ),
            html.Div(
                description[i], style={'flex': 1, 'padding': '10px', 'border': '1px solid black'}
            )
        ], style={'display': 'flex', 'flexDirection': 'row'}
        ) for i in range(n_elements)
    ]

def init_Collection(data_table, filter_table=None):
    CollectionView = CollectionViewer(data_table, filter_table)
    CollectionView.sort()
    return CollectionView

@callback(
    Output(component_id='page-collection-dummy', component_property='children'),
    Input({"type": "item", "index": ALL}, "n_clicks"),
    prevent_initial_call=True
)
def click_box(values):
    if ctx.triggered_id:  #TODO necessary?
        ix = ctx.triggered_id["index"]
        if any(values):
            if session["collection_type"] == TableType.ALBUM.name:
                CollectionView = init_Collection(config.table[TableType.ALBUM]["data_table"], session["collection"])
                # Back to default
                session_manager(
                    {
                        "album": {'ID_ALBUM': CollectionView.datatable.table.loc[ix, "ID_ALBUM"]},
                        "album_view": {"ID_PHOTO": [None]}
                    }
                )
            elif session["collection_type"] == TableType.NOTEBOOK.name:
                CollectionView = init_Collection(config.table[TableType.NOTEBOOK]["data_table"])
                session_manager(
                    {
                        "notebook": {'ID_NOTEBOOK': CollectionView.datatable.table.loc[ix, "ID_NOTEBOOK"]},
                    }
                )
                session_manager({"collection_type": TableType.NOTE.name})
            elif session["collection_type"] == TableType.NOTE.name:
                CollectionView = init_Collection(config.table[TableType.NOTE]["data_table"])
                session_manager(
                    {
                        "note": {'ID_NOTE': CollectionView.datatable.table.loc[ix, "ID_NOTE"]},
                    }
                )
    return ""


