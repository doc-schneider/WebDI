import pandas as pd
import os

from DataStructures.Document import DocumentTable
from DataOperations.Files import get_files_info
from DataStructures.TableTypes import column_types_table
from DataOperations.Photos import PhotoFactory


# class CD(DocumentTable):
#     def __init__(self, table, cover=None):
#         super().__init__(table)
#         self.cover = cover   # Filename of cover.


class MusicFactory:

    @staticmethod
    def cd_from_path(
            path_cd,
            folder_cd,
            pretable=None,
            leaveout_list=None
    ):

        # Returns TIME_CREATED, PATH, DOCUMENT_NAME, DOCUMENT_TYPE
        files_info = get_files_info(path_cd + folder_cd + "/")
        cols_fileinfo = list(files_info.columns)

        # standard columns for photo table
        cols_standard = column_types_table(
            "music",
            optional_columns=[],
            remove_primarykey=True,
            return_aliasnames=True
        )
        table = {name: [] for name in cols_standard}

        # Add columns from pretable. It is assumed that pretable deosn't contain invalid columns
        columns_add = list()
        if (pretable is not None):
            columns_pretable = list(pretable.data.columns)
            columns_add = list(set(pretable.data.columns) - set(cols_standard))
            table_add = {name: [] for name in columns_add}
            table.update(table_add)

        # Filter for allowed formats.
        # - Photos also allowed for cover
        files_info = files_info.loc[
            files_info['DOCUMENT_TYPE'].apply(
                lambda x: MusicFactory.allowed_music_formats(x) or PhotoFactory.allowed_photo_formats(x)
            )
        ]
        files_info.reset_index(inplace=True, drop=True)

        for i in range(files_info.shape[0]):

            # Basic file information
            for col in (set(cols_fileinfo) - set(["TIME_CREATED"])):
                table[col].append(
                    files_info.loc[i, col]
                )

            for col in set(cols_standard + columns_add) - set(cols_fileinfo):
                table[col].append(None)

            if (pretable is not None):
                # Match by document name
                ix = pretable.data['DOCUMENT_NAME'] == files_info.loc[i, 'DOCUMENT_NAME']
                if ix.any():
                    for col in (set(columns_pretable) - set(["DOCUMENT_NAME"])):
                        table[col][-1] = pretable.data.loc[
                            ix,
                            col
                        ].values[0]

        return DocumentTable(
            pd.DataFrame(data=table),
            document_category="music",
            table_name=folder_cd
        )

    @staticmethod
    def allowed_music_formats(input: str) -> bool:
        allowed_formats = ['m4a']
        return input.lower() in allowed_formats