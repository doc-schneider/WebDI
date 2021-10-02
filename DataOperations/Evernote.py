import os
import pandas as pd
import datetime as dtm
from pytz import timezone
from pathlib import Path
from shutil import copyfile
from distutils.dir_util import copy_tree
import xml.etree.ElementTree as ET

from DataStructures.Document import DocumentTable


class EvernoteFactory:

    @staticmethod
    # TODO PreTable, DESCRIPTION
    def table_from_path(path_root, path_note, category=None, events=None):
        # The enex file (xml) gives the meta-information, title of note.
        # Content is in the same folder as title_html and potentially title_files.
        # Default category is the Notebook name. Parent category is Notebook stack, if it exists.

        DATETIME = list()
        PATH = list()
        DOCUMENT_NAME = list()
        DOCUMENT_TYPE = list()
        TITLE = list()
        DESCRIPTION = list()
        CATEGORY = list()
        ATTACHMENT = list()
        EVENT = list()

        pth = os.path.normpath(os.path.join(path_root, path_note))
        pth_base = os.path.basename(pth)
        file_enex = pth_base + '.enex'
        path_enex = os.path.normpath(os.path.join(pth, file_enex))

        tree = ET.parse(path_enex)
        root = tree.getroot()
        for note in root:  # note is one diary unit. Oldest comes first.
            DOCUMENT_TYPE.append('html')  # Extra export from Evernote

            title = note[0].text
            TITLE.append(title)

            # html files get counter when occurring multiple times.
            # TODO max 45 correct for additional counting?
            name = title[:45]  # max 45 characters
            count = 1
            while (name + '.html') in DOCUMENT_NAME:
                count += 1
                name = title + ' [' + str(count) + ']'
            DOCUMENT_NAME.append(name + '.html')

            PATH.append((path_root + path_note).replace("\\","/"))

            created = dtm.datetime.strptime(note[2].text, '%Y%m%dT%H%M%S%z')  # date time in UTC
            created = created.astimezone(timezone('Europe/Berlin')).replace(tzinfo=None)
            DATETIME.append(created)
            # TODO ? Updated

            #  Attached documents
            if os.path.isdir(os.path.join(pth, name + "_files")):
                ATTACHMENT.append(name + "_files")
            else:
                ATTACHMENT.append(None)

            # TODO
            DESCRIPTION.append(None)

            # TODO
            if category is not None:
                CATEGORY.append(category)
            else:
                CATEGORY.append(pth_base)

            # TODO
            if events is not None:
                EVENT.append(events)
            else:
                EVENT.append(None)

        df = pd.DataFrame(data={'DATETIME': DATETIME, 'PATH': PATH,
                                'DOCUMENT_NAME': DOCUMENT_NAME, 'DOCUMENT_TYPE': DOCUMENT_TYPE,
                                'TITLE': TITLE, 'ATTACHMENT': ATTACHMENT,
                                'DESCRIPTION': DESCRIPTION,
                                'CATEGORY': CATEGORY, 'EVENT': EVENT})

        return DocumentTable(df)

    @staticmethod
    def copy_html_to_static(evernotetable, static_basepath):
        # html & _files
        # Target location: sub static base path
        ix = static_basepath.parts.index('static')
        substatic_basepath = []
        [substatic_basepath.append('/' + static_basepath.parts[i]) for i in range(ix + 1, len(static_basepath.parts))]
        substatic_basepath = ''.join(substatic_basepath)
        evernotetable.data['STATIC_PATH'] = ''    # Static paths for the documents.
        for i in range(evernotetable.length):
            row = evernotetable.data.loc[i]
            # Original location.
            p = Path(row.PATH)
            # TODO:  -2 path parts
            # Pure Evernote path = Notbook structure
            evernote_path = p.parts[-2] + '/' + p.parts[-1]
            # Target location: sub static path
            evernotetable.data.loc[i,'STATIC_PATH'] = str(Path(substatic_basepath + '/' + evernote_path))
            # Copy location in static path.
            static_path = static_basepath.joinpath(evernote_path)
            # Create directory
            try:
                os.makedirs(static_path)
            except OSError:
                pass
            nm = row.DOCUMENT_NAME
            html_orig = p.joinpath(nm + '.html')
            html_target = static_path.joinpath(nm + '.html')
            # Overwrites existing
            copyfile(str(html_orig), str(html_target))
            dir_orig = p.joinpath(nm + '_files')
            dir_target = static_path.joinpath(nm + '_files')
            copy_tree(str(dir_orig),str(dir_target))

        return evernotetable


