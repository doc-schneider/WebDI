import dash
from dash import html, Input, Output, State, callback, ctx, dcc, ALL
from flask import session

from SessionManager.ManageSessions import session_manager, show_session
from DataStructures.TableTypes import TableType
from DataOperations.Photo import allow_formats_image, allow_formats_video
from Views.Album import AlbumViewer
import config

'''
- xyz
'''

#TODO Fix
table_type = TableType.PHOTO

dash.register_page(__name__)

layout = html.Div([
    html.Br(),
    html.Div([
        html.Button('früher', id='earlier', n_clicks=0),
        html.Button('später', id='later', n_clicks=0),
    ], style={'display': 'flex', 'justify-content': 'center'}
    ),
    html.Div(id="album"),
    html.Br(),
    html.Br(),
    html.Div(
        dcc.Slider(
            min=1,
            max=240,
            value=1,
            step=1,
            id='album-slider'
        )
    ),
])

@callback(
    Output('album', 'children'),
    Output('album-slider', 'max'),
    Output('album-slider', 'value'),
    Output('album-slider', 'marks'),
    Output('store', 'data', allow_duplicate=True),
    Input('earlier', "n_clicks"),
    Input('later', "n_clicks"),
    Input('album-slider', 'value'),
    State('store', 'data'),
    prevent_initial_call=True
)
def click_button(b1, b2, value, current_data):
    #TODO session_manager
    AlbumView = init_Album(session["album"], session["album_view"])

    if ctx.triggered_id == "earlier" and b1 > 0:  #TODO ctx gives a wrong value for no click (earlier)
        AlbumView.earlier(config.table[table_type]["data_table"])
    elif ctx.triggered_id == "later" and b2 > 0:
        AlbumView.later(config.table[table_type]["data_table"])
    elif ctx.triggered_id == "album-slider":
        AlbumView.jump(config.table[table_type]["data_table"], value - 1)
    else:
        pass  # None. Initial or refresh

    current_data["album_view"]["ID_PHOTO"] = list(AlbumView.ix_show)  #TODO general identifier
    session_manager({"album_view": {"ID_PHOTO": list(AlbumView.ix_show)}})
    return update_album(AlbumView, current_data)

def update_album(AlbumView, current_data):
    boxes_dct = AlbumView.view()
    n_dim = boxes_dct["N_DIM"]
    n_boxes = boxes_dct["N_BOXES"]
    album = AlbumView.album["ALBUM"]
    chapter = boxes_dct["CHAPTER"]
    descriptions = boxes_dct["DESCRIPTION"]
    file_formats = boxes_dct["FILE_FORMAT"]

    # if config.table["table_type"].name == "PHOTO":  #TODO Fix
    content_display = boxes_dct["IMAGE"]
    date_time = boxes_dct["DATE_TIME"].dt.strftime('%Y-%m-%d %X')

    # TODO Updating slider properties which are actually fixed not so good. Should be handed over from higher level (config, store)
    slider_max = AlbumView.album["N_ELEMENTS"]
    slider_value = AlbumView.ix_show[0]
    slider_marks = {int(x)+1: y for y, x in AlbumView.album["CHAPTERS"].items()}

    # TODO The basic layout is actually fixed. Only would need to exchange the content
    return [
               html.H2(album),
               html.H3(chapter)
           ] + [
        html.Div([
            html.Div(
                media_type_box(file_formats[i], content_display[i], i, date_time[i], descriptions[i]),
                style={'flex': 1, 'padding': '10px', 'border': '1px solid black'}
            ) if i < n_boxes else html.Div(style={'flex': 1}) for i in range(r * n_dim[1], (r + 1) * n_dim[1])
        ], style={'display': 'flex', 'flexDirection': 'row'}) for r in range(n_dim[0])
    ], slider_max, slider_value, slider_marks, current_data

def media_type_box(media_type, content_display, i, date_time, description):
    # TODO Link back to main code
    if media_type in allow_formats_image:
        return [
            dcc.Link(
                html.Img(
                    src="data:image/jpeg;base64," + content_display,
                    width="100%",
                    id={"type": "box", "index": i}
                ),
                href=dash.page_registry["pages.content"]["relative_path"], refresh=False
            ),
            html.Div(date_time + ": " + description)
        ]
    elif media_type in allow_formats_video:
        return [
            dcc.Link(
                html.Video(
                    src=content_display,
                    controls=True,
                    width="100%",
                    id={"type": "box", "index": i}
                ),
                href=dash.page_registry["pages.content"]["relative_path"], refresh=False
            ),
            html.Div(date_time + ": " + description)
        ]
# n_clicks=0

def init_Album(album, album_view):
    return AlbumViewer(
        config.table[table_type]["data_table"],
        album,
        album_view
    )

@callback(
    Output('store', 'data', allow_duplicate=True),
    Input({"type": "box", "index": ALL}, "n_clicks"),
    State('store', 'data'),
    prevent_initial_call=True
)
def click_box(values, current_data):
    if ctx.triggered_id:   #TODO Do I need this?
        ix = ctx.triggered_id["index"]
        if any(values):
            AlbumView = init_Album(session["album"], session["album_view"])
            session_manager({"photo": {"ID_PHOTO": AlbumView.datatable.table.loc[ix, "ID_PHOTO"]}})
            current_data["photo"] = {'ID_PHOTO': AlbumView.datatable.table.loc[ix, "ID_PHOTO"]}
    return current_data
