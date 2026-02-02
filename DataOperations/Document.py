import pandas as pd
from pillow_heif import register_heif_opener

from DataOperations.Files import get_files_info, read_table_from_csv
from DataOperations.Helper import get_pretable, merge_pretable, allow_formats_all, get_creation_time
from DataStructures.TableTypes import TableType, table_definitions, table_columns_names_types
from DataStructures.Data import DataTable


class DocumentFactory:

    @staticmethod
    def table_from_folder(
            path_document,
            collection_name,
            chapters,
            timezone_default="CET",
            pretable_file=None
    ):
        # Create table from standard columns
        cols = list(table_definitions[TableType.DOCUMENT]["Columns"].keys())
        table = pd.DataFrame(
            columns=cols
        )

        # Get pretable
        pretable, pretable_file_name, cols_add = get_pretable(pretable_file, cols)

        # Concatenate chapters
        for i in range(len(path_document)):
            table_part = pd.DataFrame(
                columns=cols + cols_add
            )
            table_files = get_files_info(
                path_document[i],
                [],
                allow_formats_all,
                [pretable_file_name],
            )
            table_part = pd.concat([table_part, table_files], axis=0, ignore_index=True)
            table_part["CHAPTER"] = chapters[i]
            table = pd.concat([table, table_part], axis=0, ignore_index=True)

        # Get creation time
        # TODO Update to PhotoFactory
        # get_creation_time(table, timezone_default)
        # t = table.loc[i, "TIME_MODIFIED"].floor("S")   ?

        # Drop non-required columns from files info
        table.drop(columns=set(table.columns) - set(cols + cols_add), inplace=True)

        table["DOCUMENT_COLLECTION"] = collection_name

        # Merge pre-table into main table
        merge_pretable(pretable, table)

        # Crate standard table object
        document_table = DataTable(table, TableType.DOCUMENT)

        document_table.replace_nan()
        document_table.format_path()
        document_table.format_documentgroup()

        return document_table
