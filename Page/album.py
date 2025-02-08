from dash import html

from DataStructures.TableTypes import TableType
from DataOperations.Photo import allow_formats_image, allow_formats_video
from Views.Album import AlbumViewer
import config

'''
- xyz
'''

def update_album(AlbumView):
    boxes_dct = AlbumView.view()
    n_dim = boxes_dct["N_DIM"]
    n_boxes = boxes_dct["N_BOXES"]

    # TODO Updating slider properties which are actually fixed not so good. Should be handed over from higher level (config, store)
    slider_max = AlbumView.album["N_ELEMENTS"]
    slider_value = AlbumView.ix_show[0]
    slider_marks = {int(x)+1: y for y, x in AlbumView.album["CHAPTERS"].items()}

    # TODO The basic layout is actually fixed. Only would need to exchange the content
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
                    boxes_dct["DATE_TIME"]["value"].dt.strftime('%Y-%m-%d %X')[i],
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
                id={"type": "box", "index": i}
            ),
            html.Div(date_time + ": " + description)
        ]
    elif media_type in allow_formats_video:
        return [
            html.Video(
                src=content_display,
                preload='none',
                controls=True,
                width="100%",
                id={"type": "box", "index": i}
            ),
            html.Div(date_time + ": " + description)
        ]

def init_Album(album, album_view):
    return AlbumViewer(
        config.table[TableType.PHOTO]["data_table"],
        album,
        album_view
    )
