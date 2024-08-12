import pandas as pd
import numpy as np

from DataStructures.Data import DataTable
from Views.View_Factory import ViewFactory


# Definition of layout on page
n_rows = 2
n_cols = 3

class AlbumViewer():
    def __init__(self, datatable_initial, album_dct):
        self.datatable = None  # Clipped table
        self.table_type = datatable_initial.table_type

        # TODO Store complete table?
        # Which album out of the total collection?
        id_album = album_dct['ID_ALBUM']   # TODO use ForeignKey
        datatable = datatable_initial.match_foreignkey(id_album)
        datatable.sort()
        # Structure of the album
        chapters = datatable.table["CHAPTER"].unique()
        self.album = {
            "ID_ALBUM": id_album,
            "ALBUM": datatable.table.loc[0, "PHOTO_ALBUM"],
            "N_ELEMENTS": datatable.table.shape[0],
            "CHAPTERS": {}
        }
        # First element of chapter
        for c in chapters:
            self.album["CHAPTERS"][c] = datatable.table.loc[
                                        datatable.table["CHAPTER"] == c,
                                        :
                                        ].index[0]

        # Get first n indices to initialise
        self.ix_show = np.arange(np.min((n_rows * n_cols, self.album["N_ELEMENTS"])))

        self.update(datatable_initial)

    def update(self, datatable):
        datatable.sort()
        self.datatable = DataTable(
            datatable.table.loc[
                datatable.table["ID_ALBUM"] == self.album["ID_ALBUM"], :
            ].reset_index(drop=True).loc[
                self.ix_show, :
            ].reset_index(drop=True),
            self.table_type
        )

    def earlier(self, datatable):
        ix_show = self.ix_show - n_rows * n_cols
        if not np.all(~(ix_show >= 0)):  # All indices out of range? Then do nothing
            self.ix_show = ix_show[ix_show >= 0]
        self.update(datatable)

    def later(self, datatable):
        ix_show = self.ix_show + n_rows * n_cols
        if not np.all(~(ix_show < self.album["N_ELEMENTS"])):
            self.ix_show = ix_show[ix_show < self.album["N_ELEMENTS"]]  # Don't exceed last element
        self.update(datatable)

    def jump(self, datatable, ix):
        self.ix_show = np.arange(ix, np.min((ix + n_rows * n_cols, self.album["N_ELEMENTS"])))  # At least ix is valid
        self.update(datatable)

    def view(self):
        # Raw content
        boxes = ViewFactory.view(self.datatable, view_mode="ALBUM")

        # Only depict content belonging to one chapter on display page
        # TODO Should act on datatable itself, e,g in update
        chapter = boxes["CHAPTER"][0]
        ix_chapter = boxes["CHAPTER"] == chapter
        for k in boxes.keys():
            boxes[k] = boxes[k][ix_chapter]
        # How many left?
        boxes["N_BOXES"] = boxes["CHAPTER"].shape[0]

        # Information needed only once or not
        boxes["CHAPTER"] = boxes["CHAPTER"][0]
        del boxes["PHOTO_ALBUM"]

        # Dimension information for viewing  # TODO Should be in pages and config
        boxes["N_DIM"] = (n_rows, n_cols)

        return boxes
