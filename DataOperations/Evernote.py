import os
import pandas as pd
import datetime as dtm
from pytz import timezone
from pathlib import Path
from shutil import copyfile
from distutils.dir_util import copy_tree
import xml.etree.ElementTree as ET

from DataStructures.Document import DocumentTable
from DataStructures.TableTypes import column_types_table


class EvernoteFactory:

    @staticmethod
    # TODO PreTable, DESCRIPTION
    def table_from_path(
            path_root, path_note,
            pretable=None,
            optional_columns=[],
            read_date_from_title=False
    ):
        # Creates a notetable from Evernote data
        # - The enex file (xml) gives the meta-information, title of note.
        # - Content is in the same folder as title_html and potentially title_files.
        # # Default category is the Notebook name. Parent category is Notebook stack, if it exists.

        # standard + optional columns for note table
        cols_all = column_types_table(
            "note",
            optional_columns=optional_columns,
            remove_primarykey=True,
            return_aliasnames=True
        )
        table = {name: [] for name in cols_all}

        pth = os.path.normpath(os.path.join(path_root, path_note))
        pth_base = os.path.basename(pth)

        file_enex = pth_base + '.enex'
        path_enex = os.path.normpath(os.path.join(pth, file_enex))
        tree = ET.parse(path_enex)
        root = tree.getroot()
        for note in root:  # note is one diary unit. Oldest comes first.

            table["DOCUMENT_TYPE"].append('html')  # Extra export from Evernote

            title = note[0].text
            table["DOCUMENT_TITLE"].append(title)

            table["PATH"].append((path_root + path_note).replace("\\", "/") + "/")

            created = dtm.datetime.strptime(note[2].text, '%Y%m%dT%H%M%S%z')  # date time in UTC
            created = created.astimezone(timezone('Europe/Berlin')).replace(tzinfo=None)
            # TODO Created is the relevant time stamp. More time information in Udpated
            if read_date_from_title:
                # Expects yyyy-mm-dd as first characters
                try:
                    created = dtm.datetime.strptime(title[:10], "%Y-%m-%d")
                except:
                    pass
            table["DATETIME"].append(created)

            # Tag entries
            # TODO Multiple events, tags, different types,
            #  Is 4 .. always tag?
            event = None
            tag = None
            if len(note) >= 5:
                    # TODO Why is this None sometimes?
                    for i in range(4, len(note)):
                        if note[i].text is not None:  # Record containing Tag?
                            if "\\e" in note[i].text:
                                # TODO Multiple events
                                event = note[i].text.replace("\\e ", "")
                            elif "\\t" in note[i].text:
                                if tag is None:
                                    tag = note[i].text.replace("\\t ", "")
                                else:
                                    tag = tag + "|" + note[i].text.replace("\\t ", "")
                            else:
                                # Old tags without \\
                                if tag is None:
                                    tag = note[i].text
                                else:
                                    tag = tag + "|" + note[i].text
            if "EVENT" in cols_all:
                table["EVENT"].append(event)
            table["TAG"].append(tag)

            # html files get counter when occurring multiple times.
            # TODO max 45 correct for additional counting?
            name = title[:45]  # max 45 characters
            count = 1
            while (name + '.html') in table["DOCUMENT_NAME"]:
                count += 1
                name = title + ' [' + str(count) + ']'
            table["DOCUMENT_NAME"].append(name + '.html')

            #  Attached documents
            if os.path.isdir(os.path.join(pth, name + "_files")):
                table["ATTACHMENT"].append(name + "_files")
            else:
                table["ATTACHMENT"].append(None)

            for col in (set(cols_all) - set([
                "ATTACHMENT", "DOCUMENT_NAME", "DATETIME", "PATH", "DOCUMENT_TITLE",
                "DOCUMENT_TYPE", "TAG", "EVENT"
            ])):
                table[col].append(None)

        return DocumentTable(
            pd.DataFrame(data=table),
            document_category="note",
            table_name=path_note
        )

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



