from dash import html, Input, Output, callback, ctx, dcc, ALL
from flask import session

from DataStructures.TableTypes import TableType
from pages.timeline import init_Timeline


# Click  box for redirect
@callback(
    Output("url-redirect", "href"),
    [
        Input({"type": "album_box", "index": ALL}, "n_clicks"),
        Input({"type": "box-timeline", "index": ALL}, "n_clicks"),
    ],
    prevent_initial_call=True
)
def click_box(n_clicks_list_photo, n_clicks_list_timeline):
    if any(c is not None for c in n_clicks_list_photo):
        ix = ctx.triggered_id["index"]
        session["content_content"] = TableType.PHOTO.name
        #AlbumView = init_Album(session['ALBUM'], session["album_view"])
        #session['content_view']["ID_PHOTO"] = AlbumView.datatable_show.table.loc[ix, "ID_PHOTO"]
        return "/content"
    elif any(c is not None for c in n_clicks_list_timeline):
        ix = ctx.triggered_id["index"]
        TimelineView = init_Timeline(
            session['timeline_content'],
            session["timeline_view"],
        )
        id_album = TimelineView.datatable_show.table.loc[ix, "ID_ALBUM"]
        session['ALBUM']["ID_ALBUM"] = id_album
        session['album_view'] = {"IX_PHOTO": [None]}
        return "/album"

# elif any(c is not None for c in n_clicks_list_table):
#     ix = clicked["index"]
#     CollectionView = init_Collection(
#         config.table[TableType.ALBUM]["data_table"]
#     )
#     id_album = CollectionView.datatable.table.loc[ix, "ID_ALBUM"]
#     session['ALBUM']["ID_ALBUM"] = id_album
#     session['album_view'] = {"IX_PHOTO": [None]}
