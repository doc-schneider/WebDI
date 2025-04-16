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


class EvernoteFactory:

    @staticmethod
    def table_from_folder(
            path_notebook
    ):
        # Create table from standard columns
        cols = list(table_definitions[TableType.NOTE]["Columns"].keys())
        table = {name: [] for name in cols}

        tree = ET.parse(path_notebook)
        root = tree.getroot()
        for note in root:  # note is one diary unit.
            # Notebook name is file name
            table["NOTEBOOK"].append(path_notebook.stem)
            table["FILE_FORMAT"].append("html")
            table["PATH"].append(path_notebook.parent)

            for child in note:
                flag_attachment = False
                if child.tag == "title":
                    table["TITLE"].append(child.text)
                elif child.tag == "created":
                    t = pd.to_datetime(child.text, format='%Y%m%dT%H%M%S%z')
                    # TODO For notes written in not CET zone
                    timezone_default = "CET"
                    t = t.tz_convert(timezone_default)
                    table["DATE_TIME"].append(t.tz_localize(None))
                elif child.tag == "updated":
                    pass
                elif child.tag == "resource":
                    flag_attachment = True

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

        #
        # # standard + optional columns for note table
        # cols_all = column_types_table(
        #     "note",
        #     optional_columns=optional_columns,
        #     remove_primarykey=True,
        #     return_aliasnames=True
        # )
        # table = {name: [] for name in cols_all}
        #
        # pth = os.path.normpath(os.path.join(path_root, path_note))
        # pth_base = os.path.basename(pth)
        #
        # file_enex = pth_base + '.enex'
        # path_enex = os.path.normpath(os.path.join(pth, file_enex))
        # tree = ET.parse(path_enex)
        # root = tree.getroot()
        # for note in root:  # note is one diary unit. Oldest comes first.
        #
        #     table["DOCUMENT_TYPE"].append('html')  # Extra export from Evernote
        #
        #     title = note[0].text
        #     table["DOCUMENT_TITLE"].append(title)
        #
        #     table["PATH"].append((path_root + path_note).replace("\\", "/") + "/")
        #
        #     created = dtm.datetime.strptime(note[2].text, '%Y%m%dT%H%M%S%z')  # date time in UTC
        #     created = created.astimezone(timezone('Europe/Berlin')).replace(tzinfo=None)
        #     # TODO Created is the relevant time stamp. More time information in Udpated
        #     if read_date_from_title:
        #         # Expects yyyy-mm-dd as first characters
        #         try:
        #             created = dtm.datetime.strptime(title[:10], "%Y-%m-%d")
        #         except:
        #             pass
        #     table["DATETIME"].append(created)
        #
        #     # Tag entries
        #     # TODO Multiple events, tags, different types,
        #     #  Is 4 .. always tag?
        #     event = None
        #     tag = None
        #     if len(note) >= 5:
        #             # TODO Why is this None sometimes?
        #             for i in range(4, len(note)):
        #                 if note[i].text is not None:  # Record containing Tag?
        #                     if "\\e" in note[i].text:
        #                         # TODO Multiple events
        #                         event = note[i].text.replace("\\e ", "")
        #                     elif "\\t" in note[i].text:
        #                         if tag is None:
        #                             tag = note[i].text.replace("\\t ", "")
        #                         else:
        #                             tag = tag + "|" + note[i].text.replace("\\t ", "")
        #                     else:
        #                         # Old tags without \\
        #                         if tag is None:
        #                             tag = note[i].text
        #                         else:
        #                             tag = tag + "|" + note[i].text
        #     if "EVENT" in cols_all:
        #         table["EVENT"].append(event)
        #     table["TAG"].append(tag)
        #
        #     # html files get counter when occurring multiple times.
        #     # TODO max 45 correct for additional counting?
        #     name = title[:45]  # max 45 characters
        #     count = 1
        #     while (name + '.html') in table["DOCUMENT_NAME"]:
        #         count += 1
        #         name = title + ' [' + str(count) + ']'
        #     table["DOCUMENT_NAME"].append(name + '.html')
        #
        #     #  Attached documents
        #     if os.path.isdir(os.path.join(pth, name + "_files")):
        #         table["ATTACHMENT"].append(name + "_files")
        #     else:
        #         table["ATTACHMENT"].append(None)
        #
        #     for col in (set(cols_all) - set([
        #         "ATTACHMENT", "DOCUMENT_NAME", "DATETIME", "PATH", "DOCUMENT_TITLE",
        #         "DOCUMENT_TYPE", "TAG", "EVENT"
        #     ])):
        #         table[col].append(None)
        #
        # return DocumentTable(
        #     pd.DataFrame(data=table),
        #     document_category="note",
        #     table_name=path_note
        # )

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

class NotebookFactory:

    @staticmethod
    def table_from_folder(
            path_notebook
    ):

