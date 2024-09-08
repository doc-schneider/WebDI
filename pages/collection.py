import dash
from dash import html, Input, Output, State, ctx, ALL, callback, dcc

from Views.Collection import CollectionViewer
from DataStructures.TableTypes import TableType
from SessionManager.ManageSessions import session_manager, show_session
import config

'''
- xyz
'''


dash.register_page(__name__)

#TODO Can get rid of dummy?
layout = html.Div([
    html.Br(),
    html.Br(),
    html.Div(
        id="dummy-collection",
        n_clicks=0
    ),
    html.Div(
        id="collection"
    )
])

@callback(
    Output(component_id='collection', component_property='children'),
    Input("dummy-collection", "n_clicks")
)
def create_collection(values):
    show_session("collection create")
    CollectionView = init_Collection(config.table[TableType.ALBUM]["data_table"])
    collection_dct = CollectionView.view()
    descriptions = collection_dct["DESCRIPTION"]
    n_elements = CollectionView.collection["N_ELEMENTS"]

    # if config.table["table_type"].name == "ALBUM":  # TODO Content type is relevant here: book etc
    content_display = collection_dct["PHOTO_ALBUM"]
    date_from = collection_dct["DATE_FROM"].dt.strftime('%Y-%m-%d %X')
    date_to = collection_dct["DATE_TO"].dt.strftime('%Y-%m-%d %X')

    return [
        html.Div([
            html.Div(
                date_from[i], style={'flex': 1, 'padding': '10px', 'border': '1px solid black'}
            ),
            html.Div(
                date_to[i], style={'flex': 1, 'padding': '10px', 'border': '1px solid black'}
            ),
            dcc.Link(
                html.Div(
                    content_display[i],
                    style={'backgroundColor': '#aaffaa', 'flex': 1, 'padding': '10px', 'border': '1px solid black'},
                    id={"type": "item", "index": i}
                ),
                href=dash.page_registry["pages.album"]["relative_path"], refresh=False
            ),
            html.Div(
                descriptions[i], style={'flex': 1, 'padding': '10px', 'border': '1px solid black'}
            )
        ], style={'display': 'flex', 'flexDirection': 'row'}
        ) for i in range(n_elements)
    ]

def init_Collection(data_table):
    CollectionView = CollectionViewer(data_table)
    CollectionView.sort("DATE_FROM")
    return CollectionView

@callback(
    Output('store', 'data', allow_duplicate=True),
    Input({"type": "item", "index": ALL}, "n_clicks"),
    State('store', 'data'),
    prevent_initial_call=True
)
def click_box(values, current_data):
    show_session("collection click in")
    if ctx.triggered_id:  #TODO 2 if necessary?
        ix = ctx.triggered_id["index"]
        if any(values):
            print("collection click", ix)
            CollectionView = init_Collection(config.table[TableType.ALBUM]["data_table"])
            # Back to default
            #TODO: Use PrimaryKey
            session_manager(
                {
                    "album": {'ID_ALBUM': CollectionView.datatable.table.loc[ix, "ID_ALBUM"]},
                    "album_view": {"ID_PHOTO": [None]}
                }
            )
    show_session("collection click out")
    return current_data


