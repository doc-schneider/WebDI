import os
import pandas as pd
import datetime as dtm
from pytz import timezone
from pathlib import Path
from shutil import copyfile
from distutils.dir_util import copy_tree
import xml.etree.ElementTree as ET

from DataStructures.Data import DataTable
from DataStructures.TableTypes import TableType, table_definitions, table_columns_names_types


class NotebookFactory:

    # TODO How to handle cols_add
    @staticmethod
    def table_from_folder(
            path_notebook,
            notebook_type = "Evernote",
            cols_add=["TAG"],
            timezone_default="CET",
    ):

        # Create table from standard columns
        cols = list(table_definitions[TableType.NOTE]["Columns"].keys())
        table = {name: [] for name in cols + cols_add}

        if notebook_type == "Evernote":
            tree = ET.parse(path_notebook)
            root = tree.getroot()
            for note in root:  # note is one diary unit.
                # Notebook name is file name
                table["NOTEBOOK"].append(path_notebook.stem)
                table["FILE_FORMAT"].append("html")
                table["PATH"].append(path_notebook.parent)
                tag = None

                for child in note:
                    if child.tag == "title":
                        table["TITLE"].append(child.text)
                    elif child.tag == "created":
                        t = pd.to_datetime(child.text, format='%Y%m%dT%H%M%S%z')
                        # TODO For notes written in not CET zone
                        timezone_default = "CET"
                        t = t.tz_convert(timezone_default)
                        table["DATE_TIME"].append(t.tz_localize(None))
                    elif child.tag == "updated":
                        pass  # TODO What to do with this?
                    elif child.tag == "resource":
                        # TODO Anything?
                        pass
                    elif child.tag == "tag":
                        # TODO Add events etc
                        child.text
                        if "\\t" in child.text:
                            if tag is None:
                                tag = child.text.replace("\\t ", "")
                            else:
                                # Multiple tags
                                tag = tag + "|" + child.text.replace("\\t ", "")
                if "TAG" in cols_add:
                    table["TAG"].append(tag)

                # html files get counter when occurring multiple times.
                # TODO max 45 for additional counting? Better scan folder?
                name = table["TITLE"][-1]
                count = 1
                while (name + '.html') in table["FILE_NAME"]:
                    count += 1
                    name = table["TITLE"][-1] + ' [' + str(count) + ']'
                table["FILE_NAME"].append(name + '.html')

                #  Attached documents
                if os.path.isdir(Path(table["PATH"][-1], name + " files")):
                    table["ATTACHMENT"].append(Path(table["PATH"][-1], name + " files"))
                else:
                    table["ATTACHMENT"].append(None)

        note_table = DataTable(
            pd.DataFrame(data=table),
            TableType.NOTE
        )

        note_table.replace_nan()
        note_table.format_path(["PATH", "ATTACHMENT"])

        return note_table


    # TODO Into Helper?
    @staticmethod
    def copy_html_to_static(evernotetable, static_basepath):
        # TODO Only works for single row table
        # html & _files
        # Target location: sub static base path
        evernotetable['STATIC_LOCATION'] = None  # Static paths for the documents.
        # Original location.
        p = evernotetable["PATH"].values[0]
        if p is not None:
            # Pure Evernote path = Notebook structure
            # Copy location in static path.
            static_path = p[p.find("Evernote"):]
            d = evernotetable["DOCUMENT_NAME"].values[0]
            # Need to remove file name invalid symbols from title
            for invalid in [":", "?"]:
                d = d.replace(invalid, "")
            evernotetable['STATIC_LOCATION'] = static_path + d
            # Create directory
            os.makedirs(static_basepath + static_path, exist_ok=True)
            # Overwrites existing
            copyfile(
                p + d,
                static_basepath + static_path + d
            )
            if evernotetable["ATTACHMENT"].values[0] is not None:
                copy_tree(
                    p + evernotetable["ATTACHMENT"].values[0],
                    static_basepath + static_path + evernotetable["ATTACHMENT"].values[0]
                )



