import pandas as pd
import numpy as np

from DataStructures.TableTypes import TableType
from Views.View_Factory import ViewFactory


class CollectionViewer():
    def __init__(self, datatable_initial, filter_table=None):
        self.datatable = datatable_initial.filter(filter_table)
        self.table_type = datatable_initial.table_type
        self.collection = {
            "N_ELEMENTS":  self.datatable.table.shape[0]
        }

    def sort(self, column=None):
        if column:
            self.datatable.sort(column)
        else:
            if self.table_type in [TableType.ALBUM, TableType.NOTEBOOK, TableType.DOCUMENT_COLLECTION]:
                self.datatable.sort("DATE_FROM")
            elif self.table_type in [TableType.PHOTO, TableType.NOTE, TableType.DOCUMENT]:
                self.datatable.sort("DATE_TIME")
            else:
                pass

    def view(self):
        # All content
        dct = ViewFactory.view(self.datatable, load_media=False)
        # Table relevant entries
        boxes = {}
        if self.table_type == TableType.ALBUM:
            boxes["DATE_FROM"] = dct["DATE_FROM"]
            boxes['DATE_TO'] = dct['DATE_TO']
            boxes['PHOTO_ALBUM'] = dct['PHOTO_ALBUM']
            boxes['DESCRIPTION'] = dct['DESCRIPTION']
        else:
            pass
        return boxes
