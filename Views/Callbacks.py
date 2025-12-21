from dash import Input, Output, callback, ctx, dcc, ALL
from flask import session

from DataStructures.TableTypes import TableType
from pages.table import init_Table
from pages.timeline import init_Timeline
from pages.album import init_Album


# Click  box for redirect
@callback(
    Output("url-redirect", "href"),
    [
        Input({"type": "album_box", "index": ALL}, "n_clicks"),
        Input({"type": "box-timeline", "index": ALL}, "n_clicks"),
        Input({"type": "box-table", "index": ALL}, "n_clicks"),
    ],
    prevent_initial_call=True
)
def click_box(n_clicks_list_album, n_clicks_list_timeline, n_clicks_list_table):
    if any(c is not None for c in n_clicks_list_album):
        ix = ctx.triggered_id["index"]
        session["content_content"] = TableType.PHOTO.name
        AlbumView = init_Album(session['ALBUM'], session["album_view"])
        session['content_view']["ID_PHOTO"] = AlbumView.datatable_show.table.loc[ix, "ID_PHOTO"]
        return "/content"
    elif any(c is not None for c in n_clicks_list_timeline):
        ix = ctx.triggered_id["index"]
        TimelineView = init_Timeline(
            session['timeline_content'],
            session["timeline_view"],
        )
        if TimelineView.datatable_show.table_type.name == TableType.ALBUM.name:
            id_album = TimelineView.datatable_show.table.loc[ix, "ID_ALBUM"]
            session['ALBUM']["ID_ALBUM"] = id_album
            session['album_view'] = {"IX_PHOTO": [None]}
            return "/album"
        elif TimelineView.datatable_show.table_type.name == TableType.MESSAGE.name:
            session["content_content"] = TableType.MESSAGE.name
            id_message = TimelineView.datatable_show.table.loc[ix, "ID_MESSAGE"]
            session['content_view']["ID_MESSAGE"] = id_message
            return "/content"
        elif TimelineView.datatable_show.table_type.name == TableType.NOTE.name:
            session["content_content"] = TableType.NOTE.name
            id_message = TimelineView.datatable_show.table.loc[ix, "ID_NOTE"]
            session['content_view']["ID_NOTE"] = id_message
            return "/content"
    elif any(c is not None for c in n_clicks_list_table):
        ix = ctx.triggered_id["index"]
        TableView = init_Table(session['table_content'])
        # TODO General Table content
        id_film = TableView.datatable.table.loc[ix, "ID_FILM"]
        session["content_content"] = session['table_content']
        session['FILM']["ID_FILM"] = id_film
        session['content_view'] = {"ID_FILM": id_film}
        return "/content"



