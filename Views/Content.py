from pathlib import Path

from DataStructures.TableTypes import TableType, table_definitions
from DataStructures.Data import DataTable
from Views.View_Factory import ViewFactory
from DataOperations.Notebook import NotebookFactory
import config


class ContentViewer():
    def __init__(self, datatable, id_row):
        self.datatable = datatable
        self.datatable_show = None
        self.table_type = datatable.table_type
        self.id = id_row
        self.update()

    def update(self):
        primary_key = table_definitions[self.table_type]["PrimaryKey"]
        self.datatable_show = DataTable(
            self.datatable.table.loc[
            self.datatable.table[primary_key] == self.id, :
            ].reset_index(drop=True),
            self.table_type
        )
        # TODO Temporary fix for NOTE
        if self.table_type.name == "NOTE":
            id_notebook = self.datatable_show.table["ID_NOTEBOOK"].values[0]
            parent_table = config.table[TableType.NOTEBOOK]["data_table"].table
            file_enex = parent_table.loc[
                parent_table["ID_NOTEBOOK"] == id_notebook,
                ["FILE_NAME", "PATH"]
            ]
            enex_str = NotebookFactory.find_element_enex(
                Path(file_enex["PATH"].values[0]) / file_enex["FILE_NAME"].values[0],
                {"title": self.datatable_show.table["TITLE"].values[0]},
                "content"
            )
            self.datatable_show.table["TEXT"] = NotebookFactory.enex_to_markdown(enex_str)

    def view(self):
        boxes = ViewFactory.view(self.datatable_show)
        return boxes
