import os
import pandas as pd

from DataOperations.Files import get_files_info


class DocumentFactory:

    @staticmethod
    def table_from_folder(
            path,
            pretable_matching,
            eventtable_matching
    ):

        # Returns TIME_CREATED, PATH, DOCUMENT_NAME, DOCUMENT_TYPE
        # Exclude predocument lists and alreaday generated file lists
        # TODO More specific about exclusion
        table_files = get_files_info(
            path + "/",
            exclude_formats="csv"
        )

        # standard columns
        table_files["DESCRIPTION"] = None
        table_files["DOCUMENT_GROUP"] = None

        # Match pretable entries by file name
        if pretable_matching["pretable"] is not None:
            table_files[pretable_matching] = None
            for n in pretable_matching["pretable"]["DOCUMENT_NAME"]:
                for m in pretable_matching:
                    table_files.loc[
                        table_files["DOCUMENT_NAME"] == n,
                        m
                    ] = pretable_matching["pretable"].loc[
                        pretable_matching["pretable"]["DOCUMENT_NAME"] == n,
                        m
                    ]

        # Document Groups
        group_ix = 0
        # iphone snaps
        for f in table_files.loc[
            table_files["DOCUMENT_FORMAT"] == "MOV",
            "DOCUMENT_NAME"
        ]:
            if (table_files["DOCUMENT_NAME"] == f[:-4] + ".JPG").any():
                table_files.loc[
                    table_files["DOCUMENT_NAME"] == f[:-4] + ".JPG",
                "DOCUMENT_GROUP"
                ] = group_ix
                table_files.loc[
                    table_files["DOCUMENT_NAME"] == f[:-4] + ".MOV",
                    "DOCUMENT_GROUP"
                ] = group_ix
                group_ix = ++ 1

        # Events
        table_files["EVENT_NAME"] = None
        if eventtable_matching["matching"] == "date":
            # Find event whose time interval is overlapping
            # TODO Problems with non-exact match
            et = eventtable_matching["eventtable"][
                (~ eventtable_matching["eventtable"]["TIME_FROM"].isnull()) &
                (~ eventtable_matching["eventtable"]["TIME_TO"].isnull())
                ]  # Remove non-date lines
            table_files["EVENT_NAME"] = et.loc[
                pd.IntervalIndex.from_arrays(
                    et['TIME_FROM'],
                    et['TIME_TO'], closed='both'
                ).overlaps(
                    pd.Interval(
                        table_files["TIME_CREATED"].min(),
                        table_files["TIME_CREATED"].max(),
                        closed="both"
                    )
                ),
                "EVENT_NAME"
            ].values
        elif eventtable_matching["matching"] == "name":
            table_files["EVENT_NAME"] = eventtable_matching["eventname"]
        else:
            # TODO Other matching modes
            pass

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