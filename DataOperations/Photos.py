import pandas as pd
import numpy as np
from PIL import Image
from os import path
import datetime as dtm
import base64
from io import BytesIO

from DataStructures.Document import DocumentTable
from DataOperations.Files import get_files_info
from DataStructures.TableTypes import column_types_table


class PhotoFactory:
    # TODO: iPhone HEVC, MOV

    @staticmethod
    def table_from_folder(
            path_photo,
            folder_photo,
            pretable=None,
            transfer_events=False,
            event=None
    ):

        # Returns TIME_CREATED, PATH, DOCUMENT_NAME, DOCUMENT_TYPE
        files_info = get_files_info(path_photo + folder_photo + "/")
        cols_fileinfo = list(files_info.columns)

        # standard columns for photo table
        cols_standard = column_types_table(
            "photo",
            optional_columns=[],
            remove_primarykey=True,
            return_aliasnames=True
        )
        table = {name: [] for name in cols_standard}

        # Add columns from pretable. It is assumet that pretable deosn't contain invalid columns
        columns_add = list()
        if (pretable is not None):
            columns_pretable = list(pretable.data.columns)
            columns_add = list(set(pretable.data.columns) - set(cols_standard))
            table_add = {name: [] for name in columns_add}
            table.update(table_add)

        # Filter for photo formats.
        files_info = files_info.loc[
            files_info['DOCUMENT_TYPE'].apply(lambda x: PhotoFactory.allowed_photo_formats(x))
        ]
        files_info.reset_index(inplace=True, drop=True)

        for i in range(files_info.shape[0]):

            # Datetime created
            # TODO EXIF extractor only works for jpg (?)
            if files_info.loc[i, 'DOCUMENT_TYPE'].lower() in ['jpg', 'jpeg']:
                image = Image.open(files_info.loc[i, 'PATH'] + files_info.loc[i, 'DOCUMENT_NAME'])
                exifdata = image.getexif()
                # TODO Not precise enough due to lack of seconds. Order of photos can be distorted
                table["DATETIME"].append(
                    dtm.datetime.strptime(exifdata.get(36867), "%Y:%m:%d %H:%M:%S")
                )
            else:
                table["DATETIME"].append(
                    files_info.loc[i, 'TIME_CREATED']
                )

            for col in (set(cols_fileinfo) - set(["TIME_CREATED"])):
                table[col].append(
                    files_info.loc[i, col]
                )

            for col in set(cols_standard + columns_add) - set(cols_fileinfo) - set(["DATETIME"]):
                table[col].append(None)

            if (pretable is not None):
                # Match by document name
                ix = pretable.data['DOCUMENT_NAME'] == files_info.loc[i, 'DOCUMENT_NAME']
                if ix.any():
                    for col in (set(columns_pretable) - set(["DOCUMENT_NAME", "DATETIME"])):
                        table[col][-1] = pretable.data.loc[
                            ix,
                            col
                        ].values[0]

        if transfer_events:
            # TODO Interpoalte events?
            event = (set(table["EVENT"]) - set([None])).pop()  # Assume single event
            table["EVENT"] = [e if e is not None else event for e in table["EVENT"]]
        elif event is not None:
            table["EVENT"] = event

        return DocumentTable(
            pd.DataFrame(data=table),
            document_category="photo",
            table_name=folder_photo
        )

    @staticmethod
    def allowed_photo_formats(input: str) -> bool:
        allowed_formats = ['jpg', 'jpeg']   # 'mov'
        return input.lower() in allowed_formats

    # TODO Thumbnail in APP1 marker / exif (?). However, base64 (and open?)
    #  seems to take most time, thumbnail seems fast
    # TODO Encoding to DataOperations / File
    @staticmethod
    def load_thumbnail(file, encode_type):
        if (file is not None) and (file is not np.nan) and path.isfile(file):
            image = Image.open(file)
            image.thumbnail((512, 512))
            if encode_type == 'base64':
                buffered = BytesIO()
                image.save(buffered, format="JPEG")
                data = base64.b64encode(buffered.getvalue()).decode('ascii')
        else:
            data = None
        return data
