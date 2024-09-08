import dash
from dash import html, Input, Output, callback
from flask import session

from DataOperations.Photo import allow_formats_image, allow_formats_video
from DataStructures.Data import DataTable
from DataStructures.TableTypes import TableType, table_definitions
from Views.Content import ContentViewer
import config

#TODO Fix
table_type = TableType.PHOTO

dash.register_page(__name__)

layout = html.Div([
    html.H1('Content'),
    html.Hr(),
    html.Div(id='content')
])

@callback(
    Output('content', 'children'),
    Input('store', 'data')
)
def update_content(current_data):
    # TODO Enable general types
    ContentView = init_Content(session["photo"])
    content_dct = ContentView.view()
    if content_dct["FILE_FORMAT"][0] in allow_formats_image:
        return html.Div([
            html.Img(src="data:image/jpeg;base64," + content_dct["IMAGE"][0], width="100%"),
            html.Div(content_dct["DESCRIPTION"][0])
        ])
    elif content_dct["FILE_FORMAT"][0] in allow_formats_video:
        return html.Div([
            html.Video(
                src=content_dct["IMAGE"][0],
                controls=True,
                width="100%",
            ),
            html.Div(content_dct["DESCRIPTION"][0])
        ])

def init_Content(id):
    primary_key = table_definitions[table_type]["PrimaryKey"]
    # TODO Row selection shoudl be in Viewer
    return ContentViewer(
        DataTable(
            config.table[table_type]["data_table"].table.loc[
                config.table[table_type]["data_table"].table[primary_key] == id[primary_key],
                :
            ].reset_index(drop=True),
            table_type
        )
    )

