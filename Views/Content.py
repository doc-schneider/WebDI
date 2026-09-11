from pathlib import Path
import pandas as pd

from DataStructures.TableTypes import TableType, table_definitions
from DataStructures.Data import DataTable
from Views.View_Factory import ViewFactory
from DataOperations.Notebook import NotebookFactory
import config

date_format_German = '%d.%m.%Y %H:%M:%S'
time_format_German = "%H:%M:%S"

class ContentViewer():
    def __init__(self, datatable, content_view, datatable_additional=None):
        self.datatable = datatable
        self.table_type = datatable.table_type
        self.primary_key = table_definitions[self.table_type]["PrimaryKey"]
        self.datatable_show = None
        if self.table_type.name == "DOCUMENT":
            self.chapter = content_view["CHAPTER"]
            self.datatable_pre = self.datatable.filter({"CHAPTER": self.chapter})
            self.n_items = self.datatable_pre.table.shape[0]
            self.ix_show = content_view["IX_DOCUMENT"]
        else:
            self.ID = content_view[self.primary_key]
            self.n_items = 1
            self.ix_show = 0
        self.datatable_additional = datatable_additional
        self.table_film_content = None
        self.update()

    def update(self):
        if self.table_type.name == "DOCUMENT":
            self.datatable_show = DataTable(
                self.datatable_pre.table.loc[[self.ix_show], :].reset_index(drop=True),
                self.table_type
            )
        else:
            self.datatable_show = DataTable(
                self.datatable.table.loc[
                self.datatable.table[self.primary_key] == self.ID,
                :
                ].reset_index(drop=True),
                self.table_type
            )

        # TODO Temporary fix for NOTE, should be in central code
        if self.table_type.name == "NOTE":
            id_notebook = self.datatable_show.table["ID_NOTEBOOK"].values[0]
            parent_table = config.table[TableType.NOTEBOOK]["data_table"].table
            file_enex = parent_table.loc[
                parent_table["ID_NOTEBOOK"] == id_notebook,
                ["FILE_NAME", "PATH"]
            ]
            # TODO Only searching for title can be ambigous
            enex_element = NotebookFactory.find_element_enex(
                Path(file_enex["PATH"].values[0]) / file_enex["FILE_NAME"].values[0],
                {"title": self.datatable_show.table["TITLE"].values[0]},
            )
            # TODO Directly into MARKDOWN
            self.datatable_show.table["TEXT"], self.datatable_show.table["IMAGE"], self.datatable_show.table["FILE_FORMAT"] = NotebookFactory.process_enex(
                enex_element
            )
        elif self.table_type.name == "FILM":
            if self.datatable_additional:
                # Formatting for table
                self.table_film_content = self.datatable_additional.table[
                    ["CHAPTER", "DATE_FROM", "DATE_TO", "TIME_FROM", "TIME_TO", "DESCRIPTION"]
                ].rename(columns={"CHAPTER": "Kapitel", "DATE_FROM": "Datum Beginn", "DATE_TO": "Datum Ende",
                                  "TIME_FROM": "Start", "TIME_TO": "Stopp", "DESCRIPTION": "Beschreibung"})
                # TODO Formatting should not be here?
                self.table_film_content["Datum Beginn"] = self.table_film_content["Datum Beginn"].dt.strftime(date_format_German).fillna('')
                self.table_film_content["Datum Ende"] = self.table_film_content["Datum Ende"].dt.strftime(date_format_German).fillna('')
                self.table_film_content["Start"] = self.table_film_content["Start"].apply(lambda t: t.strftime(time_format_German))
                self.table_film_content["Stopp"] = self.table_film_content["Stopp"].apply(lambda t: t.strftime(time_format_German))
            else:
                pass  # TODO: What?

    def earlier(self):
        if self.ix_show == 0:
            self.ix_show = self.n_items - 1
        else:
            self.ix_show = self.ix_show - 1
        self.update()
    def later(self):
        self.ix_show = (self.ix_show + 1) % self.n_items
        self.update()

    def view(self):
        boxes = ViewFactory.view(self.datatable_show)
        return boxes, self.table_film_content
