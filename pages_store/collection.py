import dash
from dash import html, Input, Output, State, ctx, ALL, callback, dcc

from Views.Collection import CollectionViewer
from DataStructures.TableTypes import TableType
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
    # TODO Distinction should be made in Collection. Here uniform data types
    CollectionView = init_Collection(
        config.table[TableType.NOTEBOOK]["data_table"]
    )
    link_page = "pages.home"  # "pages.album"
    collection_dct = CollectionView.view()
    title = collection_dct["TITLE"]["value"]
    #description = collection_dct["TEXT"]
    #date_time_0 = collection_dct["DATE_TIME_0"]["value"].dt.strftime('%Y-%m-%d %X')
    #date_time_1 = collection_dct["DATE_TIME_1"]["value"].dt.strftime('%Y-%m-%d %X')
    n_elements = CollectionView.collection["N_ELEMENTS"]

    return [
        html.Div([
            html.Div(
                title[i],
                style={'backgroundColor': '#aaffaa', 'flex': 1, 'padding': '10px', 'border': '1px solid black'},
                id={"type": "item", "index": i}
            ),
        ], style={'display': 'flex', 'flexDirection': 'row'}
        ) for i in range(n_elements)
    ]
# dcc.Link(
#     html.Div(
#         title[i],
#         style={'backgroundColor': '#aaffaa', 'flex': 1, 'padding': '10px', 'border': '1px solid black'},
#         id={"type": "item", "index": i}
#     ),
#     href=dash.page_registry[link_page]["relative_path"], refresh=True
# ),

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
    if ctx.triggered_id:  #TODO What does this do?
        print("pre")
        ix = ctx.triggered_id["index"]
        if any(values):
            print(values)
    return ""


