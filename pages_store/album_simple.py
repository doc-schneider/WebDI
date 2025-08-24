import dash
from dash import html, Input, Output, State, callback, ctx, dcc, ALL, MATCH
from flask import session

from DataStructures.TableTypes import TableType
from DataOperations.Photo import allow_formats_image, allow_formats_video
from Views.Album import AlbumViewer
from Views.Collection import CollectionViewer
import config

'''
- xyz
'''


dash.register_page(__name__)

layout = html.Div([
    html.Br(),
    html.Div([
        html.Button('Alben', id='button_go_albums', n_clicks=0),
        html.Button('Fotos', id='button_go_photos', n_clicks=0),
    ], style={'display': 'flex', 'justify-content': 'center'}
    ),
    html.Br(),
    html.Div(id="album-main"),
    html.Br(),
])

@callback(
    Output('album-main', 'children'),
    Input('button_go_albums', "n_clicks"),
    Input('button_go_photos', "n_clicks"),
    Input({"type": "table_row", "index": ALL}, "n_clicks"),
)
def click_main(b1, b2, n_clicks_list_table):
    clicked = ctx.triggered_id
    if ctx.triggered_id == "button_go_photos":
        return layout_photos
    elif any(c is not None for c in n_clicks_list_table):
        ix = clicked["index"]
        CollectionView = init_Collection(
            config.table[TableType.ALBUM]["data_table"]
        )
        id_album = CollectionView.datatable.table.loc[ix, "ID_ALBUM"]
        session['ALBUM']["ID_ALBUM"] = id_album
        session['album_view'] = {"IX_PHOTO": [None]}
        return layout_photos
    else:   # Initial & button
        return create_albums()

# Album collection
# TODO Separate layout?

def create_albums():
    CollectionView = init_Collection(
        config.table[TableType.ALBUM]["data_table"]
    )
    collection_dct = CollectionView.view()
    n_elements = CollectionView.collection["N_ELEMENTS"]
    #TODO add headers
    show_table = []
    for n in range(n_elements):
        show_table.append(
            html.Div(
                [],
                style={'display': 'flex', 'flexDirection': 'row'}, id={"type": "table_row", "index": n},
            )
        )
        for k in collection_dct.keys():
            if collection_dct[k]["mysqltype"] == "datetime":
                show_table[-1].children.append(
                    html.Div(
                        collection_dct[k]["value"][n].strftime('%Y-%m-%d %X'), style={'flex': 1, 'padding': '10px', 'border': '1px solid black'}
                    )
                )
            elif collection_dct[k]["mysqltype"] == "text":
                show_table[-1].children.append(
                    html.Div(
                        collection_dct[k]["value"][n], style={'flex': 1, 'padding': '10px', 'border': '1px solid black'}
                    )
                )
            else:
                print("???")
    return show_table

def init_Collection(data_table, filter_table=None):
    CollectionView = CollectionViewer(data_table, filter_table)
    CollectionView.sort()
    return CollectionView

# Photos

layout_photos = html.Div([
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
def click_photos(b1, b2, slider_value):
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
               html.H3(boxes_dct["CHAPTER"]["value"][0])
           ] + [
        html.Div([
            html.Div(
                media_type_box(
                    boxes_dct["FILE_FORMAT"]["value"][i],
                    boxes_dct["IMAGE"][i],
                    i,
                    boxes_dct["DATE_TIME"]["value"].dt.strftime('%Y-%m-%d %X').fillna('')[i],
                    boxes_dct["DESCRIPTION"]["value"][i]
                ),
                style={'flex': 1, 'padding': '10px', 'border': '1px solid black'}
            ) if i < n_boxes else html.Div(style={'flex': 1}) for i in range(r * n_dim[1], (r + 1) * n_dim[1])
        ], style={'display': 'flex', 'flexDirection': 'row'}) for r in range(n_dim[0])
    ], slider_max, slider_value, slider_marks

def media_type_box(media_type, content_display, i, date_time, description):
    # TODO Link back to main code
    if media_type in allow_formats_image:
        return [
            html.Img(
                src="data:image/jpeg;base64," + content_display,
                width="100%",
            ),
            html.Div(date_time + ": " + description)
        ]
    elif media_type in allow_formats_video:
        return [
            html.Video(
                src=f"/video?name={content_display}",
                controls=True,
                width="100%",
            ),
            html.Div(date_time + ": " + description)
        ]

def init_Album(album, album_view):
    return AlbumViewer(
        config.table[TableType.PHOTO]["data_table"],
        album,
        album_view
    )


