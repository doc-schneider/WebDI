import dash
from dash import html, dcc, callback, Input, Output

from SessionManager.ManageSessions import session_manager
import config


dash.register_page(__name__, path='/')

layout = html.Div([
    html.H1('Homepage'),
    html.Br(),
    html.Br(),
    dcc.Dropdown(
        id='id-dropdown-collectiontype',
        options=[
            {'label': v.name, 'value': v.name}
            for v in config.collection_types
        ],
        value=config.collection_types[0].name,  # Default selected value
        clearable=False,
    ),
    html.Br(),
    html.Br(),
    html.Div(id='page-home-dummy', style={'display': 'none'})
])

@callback(
    Output(component_id='page-home-dummy', component_property='children'),
    Input('id-dropdown-collectiontype', 'value')
)
def create_collection(selected_value):
    session_manager()  # Init if not yet done
    session_manager({"collection_type": selected_value})
    return ""


