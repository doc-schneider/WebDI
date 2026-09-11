import dash
from dash import html, Input, Output, callback, ctx
from flask import session

from DataStructures.TableTypes import TableType
from Views.Content import ContentViewer
from Views.View_Factory import ViewFactory
from Initialize.Initialize import init_session
from Initialize.Formats import button_style
import config


def init_Content():
    # TODO How to deal with the initial session error?

    table_type = TableType[session["content_content"]]
    data_table = config.table[table_type]["data_table"]

    if table_type.name == "FILM":  # TODO This kind of logic should be defined as an external logical structure
        data_table_additional = ViewFactory.filter_table(
            config.table[TableType.FILM_CONTENT]["data_table"],
            session
        )
    else:
        data_table_additional = None

    print(session['content_view'])
    ContentView = ContentViewer(
        data_table,
        session['content_view'],
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

# TODO Normal construction
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
            html.Br(),
            html.Div(
                [
                    html.Button('zurück', id='back', n_clicks=0, style=button_style),
                    html.Button('weiter', id='next', n_clicks=0, style=button_style),
                ],
                style={'display': 'flex', 'justify-content': 'center', "gap": "25px"}
            ),
            html.Br(),
            html.Div(id="content")
        ])
# html.Div(init_Content())

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

@callback(
    Output('content', 'children'),
    Input('next', "n_clicks"),
    Input('back', "n_clicks"),
)
def select_content(b1, b2):
    table_type = TableType[session["content_content"]]
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
        session['content_view'],
        data_table_additional
    )

    if ctx.triggered_id == "next":
        ContentView.later()
    elif ctx.triggered_id == "back":
        ContentView.earlier()
    else:
        pass  # None. Initial or refresh
    session["content_view"]["IX_DOCUMENT"] = ContentView.ix_show

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
