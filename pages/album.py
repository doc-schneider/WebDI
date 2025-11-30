import dash
from dash import html, Input, Output, callback, ctx, dcc
from flask import session

from DataStructures.TableTypes import TableType
from Views.Album import AlbumViewer
from Views.View_Factory import ViewFactory
import config

'''
- xyz
'''


dash.register_page(__name__)

layout = html.Div([
    html.Br(),
    html.Div([
        html.Button('früher', id='earlier', n_clicks=0),
        html.Button('später', id='later', n_clicks=0),
    ], style={'display': 'flex', 'justify-content': 'center'}
    ),
    html.Div(id="photos"),
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
    Output('photos', 'children'),
    Output('album-slider', 'max'),
    Output('album-slider', 'value'),
    Output('album-slider', 'marks'),
    Input('earlier', "n_clicks"),
    Input('later', "n_clicks"),
    Input('album-slider', 'value')
)
def select_photos(b1, b2, slider_value):
    AlbumView = init_Album(session['ALBUM'], session["album_view"])
    if ctx.triggered_id == "earlier":  # and b1 > 0:  # TODO ctx gives a wrong value for no click (earlier)?
        AlbumView.earlier()
    elif ctx.triggered_id == "later":
        AlbumView.later()
    elif ctx.triggered_id == "album-slider":
        AlbumView.jump(slider_value - 1)
    else:
        pass  # None. Initial or refresh
    session["album_view"] = {"IX_PHOTO": list(AlbumView.ix_show)}
    return update_album(AlbumView)

def update_album(AlbumView):
    boxes_dct = AlbumView.view()
    n_dim = boxes_dct["N_DIM"]
    n_boxes = boxes_dct["N_BOXES"]
    slider_max = AlbumView.album["N_ELEMENTS"]
    slider_value = AlbumView.ix_show[0] + 1
    slider_marks = {int(x)+1: y for y, x in AlbumView.album["CHAPTERS"].items()}
    return [
               html.H2(AlbumView.album["ALBUM"]),
               html.H3(boxes_dct["CHAPTER"][0])
           ] + [
        html.Div([
            html.Div(
                ViewFactory.media_type_box(
                    boxes_dct["FILE_FORMAT"][i],
                    boxes_dct["IMAGE"][i]
                ) + [
                    html.Div(
                        boxes_dct["DATE_TIME"].dt.strftime('%Y-%m-%d %X').fillna('')[i] + ": " + boxes_dct["TEXT"][i]
                    )
                ],
                style={'flex': 1, 'padding': '10px', 'border': '1px solid black'},
                id={"type": "album_box", "index": i}
            ) if i < n_boxes else html.Div(style={'flex': 1}) for i in range(r * n_dim[1], (r + 1) * n_dim[1])
        ], style={'display': 'flex', 'flexDirection': 'row'}) for r in range(n_dim[0])
    ], slider_max, slider_value, slider_marks

def init_Album(album, album_view):
    return AlbumViewer(
        config.table[TableType.PHOTO]["data_table"],
        album,
        album_view
    )


