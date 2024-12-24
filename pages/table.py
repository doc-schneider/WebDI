import dash
from dash import html, Input, Output, callback, dcc

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
    prevent_initial_call=False
)
def create_table(selected_value_table, selected_value_event):
    TableView = init_Table(
        config.table[TableType[selected_value_table]]["data_table"],
        selected_value_event
    )
    table_dct = TableView.view()
    #TODO add headers
    show_table = []
    for n in range(TableView.collection["N_ELEMENTS"]):
        show_table.append(html.Div([], style={'display': 'flex', 'flexDirection': 'row'}))
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

def init_Table(data_table, id_event):
    if id_event > 0:
        TableView = TableViewer(data_table, {"ID_EVENT": id_event})
    else:
        # "" -> None
        TableView = TableViewer(data_table)
    TableView.sort()
    return TableView
