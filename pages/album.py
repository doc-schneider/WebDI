import dash
from dash import html, Input, Output, State, callback, ctx, dcc

from DataStructures.TableTypes import TableType
from Views.Album import AlbumViewer
import config

'''
- xyz
'''

#TODO Fix
table_type = TableType.PHOTO

dash.register_page(__name__)

layout = html.Div([
    html.Button('earlier', id='earlier', n_clicks=0),
    html.Button('later', id='later', n_clicks=0),
    html.Div(id="album"),
    html.Div(
        dcc.Slider(
            min=1,
            max=240,
            value=1,
            step=1,
            id='album-slider'
        )
    )
])

@callback(
    Output('album', 'children'),
    Output('album-slider', 'max'),
    Output('album-slider', 'value'),
    Output('album-slider', 'marks'),
    Input('earlier', "n_clicks"),
    Input('later', "n_clicks"),
    Input('album-slider', 'value'),
    State('store', 'data')
)
def click_button(b1, b2, value, current_data):
    if ctx.triggered_id == "earlier":
        config.AlbumView.earlier(config.table[table_type]["data_table"])
    elif ctx.triggered_id == "later":
        config.AlbumView.later(config.table[table_type]["data_table"])
    elif ctx.triggered_id == "album-slider":
        config.AlbumView.jump(config.table[table_type]["data_table"], value - 1)
    else:
        pass  # None. Initial or refresh

    return update_album(current_data["album"])

def update_album(album_dct):
    # Initialize at first call
    #TODO Do on higher level?
    if not hasattr(config, 'AlbumView') or (album_dct['ID_ALBUM'] != config.AlbumView.album['ID_ALBUM']):
        init_Album(album_dct)

    boxes_dct = config.AlbumView.view()
    n_dim = boxes_dct["N_DIM"]
    n_boxes = boxes_dct["N_BOXES"]
    descriptions = boxes_dct["DESCRIPTION"]
    chapter = boxes_dct["CHAPTER"]

    # if config.table["table_type"].name == "PHOTO":  #TODO Fix
    album = config.AlbumView.album["ALBUM"]
    content_display = boxes_dct["IMAGE"]
    date_time = boxes_dct["DATE_TIME"].dt.strftime('%Y-%m-%d %X')

    # TODO Updating slider properties which are actually fixed not so good. Should be handed over from higher level (config, store)
    slider_max = config.AlbumView.album["N_ELEMENTS"]
    slider_value = config.AlbumView.ix_show[0]
    slider_marks = {int(x)+1: y for y, x in config.AlbumView.album["CHAPTERS"].items()}

    # TODO The basic layout is actually fixed. Only would need to exchange the content
    return [
               html.H2(album),
               html.H3(chapter)
           ] + [
        html.Div([
            html.Div([
                html.Img(src="data:image/jpeg;base64," + content_display[i], width="100%"),
                html.Div(date_time[i] + ": " + descriptions[i])
            ], style={'flex': 1, 'padding': '10px', 'border': '1px solid black'}) if i < n_boxes else html.Div(style={'flex': 1}) for i in range(r * n_dim[1], (r + 1) * n_dim[1])
        ], style={'display': 'flex', 'flexDirection': 'row'}) for r in range(n_dim[0])
    ], slider_max, slider_value, slider_marks

def init_Album(album_dct):
    config.AlbumView = AlbumViewer(
        config.table[table_type]["data_table"],
        album_dct
    )
