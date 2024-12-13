import numpy as np

from DataStructures.Data import DataTable
from Views.View_Factory import ViewFactory


# Definition of layout on page
n_rows = 2
n_cols = 3

class AlbumViewer():
    def __init__(self, datatable_initial, album, album_view):
        self.datatable = None
        self.datatable_show = None
        self.table_type = datatable_initial.table_type

        # Which album out of the total collection?
        id_album = album['ID_ALBUM']
        self.datatable = datatable_initial.match_foreignkey(id_album)
        self.datatable.sort()
        # Structure of the album
        chapters = self.datatable.table["CHAPTER"].unique()
        self.album = {
            "ID_ALBUM": id_album,
            "ALBUM": self.datatable.table.loc[0, "PHOTO_ALBUM"],
            "N_ELEMENTS": self.datatable.table.shape[0],
            "CHAPTERS": {}
        }
        # First element of chapter
        for c in chapters:
            self.album["CHAPTERS"][c] = self.datatable.table.loc[
                                        self.datatable.table["CHAPTER"] == c,
                                        :
                                        ].index[0]
        # Location inside album
        ix_show = album_view["ID_PHOTO"]
        if ix_show[0] is None:
            # Get first n indices to initialise
            self.ix_show = np.arange(np.min((n_rows * n_cols, self.album["N_ELEMENTS"])))
        else:
            self.ix_show = np.array(ix_show)

        self.update()

    def update(self):
        # Only depict content belonging to one chapter on display page, not content from the next chapter
        chapter = self.datatable.table.loc[self.ix_show, "CHAPTER"].values[0]
        ix_chapter = np.where(self.datatable.table["CHAPTER"] == chapter)[0]
        self.ix_show = np.intersect1d(self.ix_show, ix_chapter)
        # If jumping forward between chapters: start with first element of chapter
        if ((self.ix_show[0] - ix_chapter[0]) < n_rows * n_cols) and ((self.ix_show[0] - ix_chapter[0]) > 0):
            # Don't exceed last element
            self.ix_show = np.arange(
                ix_chapter[0],
                np.min((ix_chapter[0] + n_rows * n_cols, ix_chapter[-1]))
            )

        self.datatable_show = DataTable(
            self.datatable.table.loc[
                self.ix_show, :
            ].reset_index(drop=True),
            self.table_type
        )

    def earlier(self):
        ix_show = self.ix_show[0] - n_rows * n_cols + np.arange(n_rows * n_cols)
        if not np.all(~(ix_show >= 0)):  # All indices out of range? Then do nothing
            self.ix_show = ix_show[ix_show >= 0]
        self.update()

    def later(self):
        ix_show = self.ix_show[0] + n_rows * n_cols + np.arange(n_rows * n_cols)
        if not np.all(~(ix_show < self.album["N_ELEMENTS"])):  # All indices out of range? Then do nothing
            self.ix_show = ix_show[ix_show < self.album["N_ELEMENTS"]]  # Don't exceed last element
        self.update()

    def jump(self, ix):
        self.ix_show = np.arange(ix, np.min((ix + n_rows * n_cols, self.album["N_ELEMENTS"])))  # At least ix is valid
        self.update()

    def view(self):
        # Raw content
        boxes = ViewFactory.view(self.datatable_show, view_mode="ALBUM")

        # Information needed only once or not
        boxes["N_BOXES"] = len(boxes["FILE_NAME"])
        boxes["CHAPTER"] = boxes["CHAPTER"][0]
        del boxes["PHOTO_ALBUM"]

        # Dimension information for viewing  # TODO Should be in pages and config
        boxes["N_DIM"] = (n_rows, n_cols)

        return boxes
