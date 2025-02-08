import dash
from dash import html, Input, Output, callback, dcc, ALL, State, ctx

from Views.Table import TableViewer
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
        id='id-dropdown-tabletype',
        options=[
            {'label': t.name, 'value': t.name} for t in [k for k in config.table.keys()]
        ],
        value=TableType.ALBUM.name,  # Default selected value
        clearable=False,
        style={'display': 'inline-block', 'width': 'auto', 'minWidth': '150px'},
    ),
    dcc.Dropdown(
        id='id-dropdown-event',
        options=[
            {'label': row['EVENT'], 'value': row['ID_EVENT']} for _, row in config.table[TableType.EVENT]["data_table"].table[["EVENT", "ID_EVENT"]].iterrows()
        ] + [{'label': "", 'value': 0}],
        value=0,  # Default selected value = None (no valid ID)
        clearable=False,
        style={'display': 'inline-block', 'marginLeft': '4%', 'width': 'auto', 'minWidth': '150px'},
    ),
    dcc.Dropdown(
        id='id-dropdown-tag',
        options=[
            {'label': row['TAG'], 'value': row['TAG']} for _, row in config.table[TableType.TAG]["data_table"].table[["TAG"]].iterrows()
        ] + [{'label': "", 'value': ""}],
        value="",
        clearable=False,
        style={'display': 'inline-block', 'marginLeft': '4%', 'width': 'auto', 'minWidth': '150px'},
    ),
    html.Br(),
    html.Br(),
    html.Div(
        id="table"
    ),
])

@callback(
    Output(component_id='table', component_property='children'),
    Input('id-dropdown-tabletype', 'value'),
    Input('id-dropdown-event', 'value'),
    Input('id-dropdown-tag', 'value'),
    prevent_initial_call=False
)
def create_table(selected_value_table, selected_value_event, selected_value_tag):
    TableView = init_Table(
        config.table[TableType[selected_value_table]]["data_table"],
        selected_value_event,
        selected_value_tag
    )
    table_dct = TableView.view()
    #TODO add headers
    show_table = []
    for n in range(TableView.collection["N_ELEMENTS"]):
        show_table.append(
            html.Div([], style={'display': 'flex', 'flexDirection': 'row'}, id={"type": "table_row", "index": n}),
        )
        for k in table_dct.keys():
            if table_dct[k]["mysqltype"] == "datetime":
                show_table[-1].children.append(
                    html.Div(
                        table_dct[k]["value"][n].strftime('%Y-%m-%d %X'), style={'flex': 1, 'padding': '10px', 'border': '1px solid black'}
                    )
                )
            elif table_dct[k]["mysqltype"] == "text":
                show_table[-1].children.append(
                    html.Div(
                        table_dct[k]["value"][n], style={'flex': 1, 'padding': '10px', 'border': '1px solid black'}
                    )
                )
            else:
                print("???")
    return show_table

def init_Table(data_table, id_event, tag):
    filter_table = {}
    if id_event > 0:
        filter_table["ID_EVENT"] = id_event
    if tag:
        filter_table["TAG"] = tag
    TableView = TableViewer(data_table, filter_table)
    TableView.sort()
    return TableView

@callback(
    Output('store', 'data'),
    Input({"type": "table_row", "index": ALL}, "n_clicks"),
    Input("test", "n_clicks"),
    State('store', 'data'),
    prevent_initial_call=True
)
def click_row(n_clicks_list_table, n_clicks_test, store_data):
    clicked = ctx.triggered_id
    if any(c is not None for c in n_clicks_list_table):
        print(store_data["index"])
        ix = clicked["index"]
        store_data["index"] = ix
        print("n_clicks_list: ", n_clicks_list_table, ", index: ", ix)
    else:
        print("empty")
    return store_data
