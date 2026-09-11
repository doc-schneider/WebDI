from DataStructures.Data import DataTable
from DataStructures.TableTypes import TableType
from Views.View_Factory import ViewFactory


class TableViewer():
    def __init__(self, datatable_initial):
        self.datatable = datatable_initial
        self.table_type = datatable_initial.table_type
        # TODO In a config file
        if self.table_type.name == "DOCUMENT":
            self.time_column = "DATE_TIME"
        else:
            self.time_column = "DATE_FROM"
            self.n_dim = datatable_initial.table.shape[0]
        self.datatable.sort(self.time_column)

    def view(self):

        if self.table_type.name == "DOCUMENT":
            # DOCUMENT is shown by Chapter
            self.datatable = DataTable(
                self.datatable.table[~self.datatable.table["CHAPTER"].duplicated()].reset_index(drop=True),
                TableType.DOCUMENT
            )
            self.n_dim = self.datatable.table.shape[0]
            # TODO Into View_Factory?
            dct = self.datatable.table[self.datatable.table.columns].to_dict("series")
            boxes = {}
            boxes['DATE_FROM'] = dct['DATE_TIME']
            boxes['DATE_TO'] = dct['DATE_TIME']
            boxes['TEXT'] = dct['CHAPTER']
            boxes['TEXT_ADDITIONAL'] = {}
            boxes['TEXT_ADDITIONAL'][0] = dct["DESCRIPTION"]
        else:
            boxes = ViewFactory.view(self.datatable, load_media=False)

        boxes["N_DIM"] = self.n_dim

        return boxes
