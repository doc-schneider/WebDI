import dash
from dash import html
from flask import session

from DataStructures.TableTypes import TableType, table_definitions
from Views.Content import ContentViewer
from Views.View_Factory import ViewFactory
import config

def init_Content():
    # TODO How to deal with the initial session error?
    table_type = TableType[session["content_content"]]
    primary_key = table_definitions[table_type]["PrimaryKey"]
    data_table = ViewFactory.filter_table(
        config.table[table_type]["data_table"],
        session
    )
    ContentView = ContentViewer(
        data_table,
        session['content_view'][primary_key]
    )

    boxes_dct = ContentView.view()
    return html.Div(
        ViewFactory.media_type_box(
            boxes_dct["FILE_FORMAT"][0],
            boxes_dct["IMAGE"][0]
        ) + [
            html.Div(
                boxes_dct["DATE_TIME"].dt.strftime('%Y-%m-%d %X').fillna('')[0] + ": " + boxes_dct["TEXT"][0]
            )
        ] + ViewFactory.additional_items(
            boxes_dct, 0, 'TEXT_ADDITIONAL'
        ) + ViewFactory.additional_items(
            boxes_dct, 0, 'MARKDOWN'
        ),
        style={
            'padding': '10px',
            'border': '1px solid black',
        },
    )

dash.register_page(__name__)

def layout():
    return html.Div([
        html.H1('Inhalt'),
        html.Hr(),
        init_Content()
    ])



