import pandas as pd
import numpy as np

from DataStructures.TableTypes import TableType
from Views.View_Factory import ViewFactory


class TableViewer():
    def __init__(self, datatable_initial, filter_table={}):
        self.table_type = datatable_initial.table_type
        self.datatable = datatable_initial.filter(filter_table)
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
        if self.table_type == TableType.PHOTO:
            # TODO: Date_FORM / TO?
            boxes['DATE_TIME'] = dct['DATE_TIME']
            boxes['CHAPTER'] = dct['CHAPTER']
            boxes['PHOTO_ALBUM'] = dct['PHOTO_ALBUM']
            boxes['DESCRIPTION'] = dct['DESCRIPTION']
        elif self.table_type == TableType.ALBUM:
            boxes["DATE_FROM"] = dct["DATE_FROM"]
            boxes['DATE_TO'] = dct['DATE_TO']
            boxes['PHOTO_ALBUM'] = dct['PHOTO_ALBUM']
            boxes['DESCRIPTION'] = dct['DESCRIPTION']
        elif self.table_type == TableType.NOTEBOOK:
            boxes['DATE_FROM'] = dct['DATE_FROM']
            boxes['DATE_TO'] = dct['DATE_TO']
            boxes['NOTEBOOK'] = dct['NOTEBOOK']
            boxes['NOTEBOOK_COLLECTION'] = dct['NOTEBOOK_COLLECTION']
            boxes['NOTEBOOK_TYPE'] = dct['NOTEBOOK_TYPE']
        elif self.table_type == TableType.NOTE:
            boxes['DATE_TIME'] = dct['DATE_TIME']
            boxes['TITLE'] = dct['TITLE']
            boxes['ATTACHMENT'] = dct['ATTACHMENT']
            boxes['NOTEBOOK'] = dct['NOTEBOOK']
        elif self.table_type == TableType.DOCUMENT:
            boxes['DATE_TIME'] = dct['DATE_TIME']
            boxes['CHAPTER'] = dct['CHAPTER']
            boxes['DOCUMENT_COLLECTION'] = dct['DOCUMENT_COLLECTION']
            boxes['DESCRIPTION'] = dct['DESCRIPTION']
        elif self.table_type == TableType.DOCUMENT_COLLECTION:
            boxes['DATE_FROM'] = dct['DATE_FROM']
            boxes['DATE_TO'] = dct['DATE_TO']
            boxes['DOCUMENT_COLLECTION'] = dct['DOCUMENT_COLLECTION']
            boxes['DESCRIPTION'] = dct['DESCRIPTION']
        elif self.table_type == TableType.EVENT:
            pass
        elif self.table_type == TableType.TAG:
            pass
        return boxes
