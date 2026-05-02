import dash
from dash import html
from flask import session

from DataStructures.TableTypes import TableType, table_definitions
from Views.Content import ContentViewer
from Views.View_Factory import ViewFactory
from Initialize.Initialize import init_session
import config


def init_Content():
    # TODO How to deal with the initial session error?

    table_type = TableType[session["content_content"]]
    primary_key = table_definitions[table_type]["PrimaryKey"]
    data_table = config.table[table_type]["data_table"]

    if table_type.name == "FILM":  # TODO This kind of logic should be defined as an external logical structure
        data_table_additional = ViewFactory.filter_table(
            config.table[TableType.FILM_CONTENT]["data_table"],
            session
        )
    else:
        data_table_additional = None

    ContentView = ContentViewer(
        data_table,
        session['content_view'][primary_key],
        data_table_additional
    )
    boxes_dct, additional_table = ContentView.view()

    if table_type.name == "FILM":
        return basic_box(boxes_dct) + [html.Br()] + [
            html.Table([
                html.Thead(
                    html.Tr([html.Th(col) for col in additional_table.columns])
                ),
                html.Tbody([
                    html.Tr([
                        html.Td(additional_table.iloc[i][col]) for col in additional_table.columns
                    ])
                    for i in range(len(additional_table))
                ])
            ],
                style={
                    "borderCollapse": "collapse",
                    "width": "100%"
                }
            )
        ]
    else:
        return basic_box(boxes_dct)

dash.register_page(__name__)

def layout():
    if "initialized" not in session:
        return html.Div([
            html.H1('Inhalt'),
            html.Hr()
        ])
    else:
        return html.Div([
            html.H1('Inhalt'),
            html.Hr(),
            html.Div(init_Content())
        ])

def basic_box(boxes_dct):
    return [
        html.Div(
            ViewFactory.media_type_box(
                boxes_dct["FILE_FORMAT"][0],
                boxes_dct["IMAGE"][0]
            ) + [
                html.Div(boxes_dct["TEXT"][0])
            ] + ViewFactory.additional_items(
                boxes_dct, 0, 'DATE_TIME'
            ) + ViewFactory.additional_items(
                boxes_dct, 0, 'TEXT_ADDITIONAL'
            ) + ViewFactory.additional_items(
                boxes_dct, 0, 'MARKDOWN'
            ),
            style={
                'padding': '10px',
                'border': '1px solid black',
            },
        )
    ]
