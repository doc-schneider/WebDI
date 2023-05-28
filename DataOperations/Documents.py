import os
import pandas as pd

from DataOperations.Files import get_files_info


class DocumentFactory:

    @staticmethod
    def table_from_folder(
            path,
            topic,
            pretable=None,
            pretable_matching=None
    ):

        # Returns TIME_CREATED, PATH, DOCUMENT_NAME, DOCUMENT_TYPE
        table_files = get_files_info(path + "/")

        # Remove pre-table entry if present
        table_files = table_files[
            table_files["DOCUMENT_NAME"] != "PreDokumentliste.csv"
        ]

        # DESCRIPTION as standard column
        table_files["DESCRIPTION"] = None

        # Match pretable entries by file name
        if pretable is not None:
            table_files[pretable_matching] = None
            for n in pretable["DOCUMENT_NAME"]:
                for m in pretable_matching:
                    table_files.loc[
                        table_files["DOCUMENT_NAME"] == n,
                        m
                    ] = pretable.loc[
                        pretable["DOCUMENT_NAME"] == n,
                        m
                    ]

        return table_files

    @staticmethod
    def read_pretable(pth, pretable_name="PreDokumentliste.csv"):
        # Check if pre-document list exists
        if os.path.isfile(pth + "/" + pretable_name):
            pretable = pd.read_csv(
                pth + "/" + "PreDokumentliste.csv",
                encoding='ANSI',
                sep=';'
            )
        else:
            pretable = None

        return pretable