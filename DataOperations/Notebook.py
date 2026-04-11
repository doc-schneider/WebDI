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
            notebook_type="Evernote",
            cols_add=[],  # ["TAG"] # TODO
            timezone_default="Europe/Berlin",
    ):

        # Create table from standard columns
        cols = list(table_definitions[TableType.NOTE]["Columns"].keys())
        table = {name: [] for name in cols + cols_add}
        table_test = pd.DataFrame(
            columns=cols
        )

        if notebook_type == "Evernote":
            tree = ET.parse(path_notebook)
            root = tree.getroot()
            for note in root:  # note is one diary unit.
                # Notebook name is file name
                table["NOTEBOOK"].append(path_notebook.stem)
                # table["FILE_FORMAT"].append("html")
                # table["PATH"].append(path_notebook.parent)
                tag = None

                for child in note:
                    if child.tag == "title":
                        table["TITLE"].append(child.text)
                    elif child.tag == "created":
                        t = pd.to_datetime(child.text, format='%Y%m%dT%H%M%S%z')
                        # TODO For notes written in not CET zone
                        t = t.tz_convert(timezone_default)
                        table["DATE_TIME"].append(t.tz_localize(None))
                    elif child.tag == "updated":
                        pass  # TODO What to do with this?
                    elif child.tag == "resource":
                        # TODO ? Contains eg base64 images
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
                # name = table["TITLE"][-1]
                # count = 1
                # while (name + '.html') in table["FILE_NAME"]:
                #     count += 1
                #     name = table["TITLE"][-1] + ' [' + str(count) + ']'
                # table["FILE_NAME"].append(name + '.html')
                #
                # #  Attached documents
                # if os.path.isdir(Path(table["PATH"][-1], name + " files")):
                #     table["ATTACHMENT"].append(Path(table["PATH"][-1], name + " files"))
                # else:
                #     table["ATTACHMENT"].append(None)

                table["FILE_NAME"].append(None)
                table["FILE_FORMAT"].append(None)
                table["PATH"].append(None)
                table["ATTACHMENT"].append(None)

        note_table = DataTable(
            pd.DataFrame(data=table),
            TableType.NOTE
        )

        note_table.replace_nan()
        # note_table.format_path(["PATH", "ATTACHMENT"])

        return note_table

    @staticmethod
    def find_element_enex(path_notebook, element_match):
        tree = ET.parse(path_notebook)
        root = tree.getroot()
        tag_match, value_match = next(iter(element_match.items()))
        # Alle <note>-Elemente durchlaufen
        for note in root.findall(".//note"):
            tag_text = note.find(tag_match)
            # Prüfen, ob der Titel passt
            if tag_text is not None and tag_text.text == value_match:
                return note

    @staticmethod
    def process_enex(enex_element):
        # content section
        content = enex_element.find("content").text
        content = content.strip()
        content = content[content.find("<en-note>"):]
        en_note = ET.fromstring(content)
        # alle divs extrahieren
        lines = []
        for div in en_note.findall(".//div"):
            lines.append("".join(div.itertext()).strip())
        lines = "\n".join(lines)

        # image section
        image = None
        file_format = None
        if enex_element.find("resource"):
            resource = enex_element.find("resource")
            if resource.find("mime") is not None and (resource.find("mime").text == 'image/jpeg'):
                image = resource.find("data").text.strip()
                file_format = "JPG"

        return lines, image, file_format

