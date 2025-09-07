from DataStructures.TableTypes import TableType, table_definitions
from DataStructures.Data import DataTable
from Views.View_Factory import ViewFactory


class ContentViewer():
    def __init__(self, datatable, id):
        self.datatable = datatable
        self.datatable_show = None
        self.table_type = datatable.table_type
        self.id = id
        self.update()

    def update(self):
        primary_key = table_definitions[self.table_type]["PrimaryKey"]
        self.datatable_show = DataTable(
            self.datatable.table.loc[
            self.datatable.table[primary_key] == self.id, :
            ].reset_index(drop=True),
            self.table_type
        )

    def view(self):
        dct = ViewFactory.view(self.datatable_show)
        return dct
