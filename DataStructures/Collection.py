import pandas as pd

from DataStructures.Document import DocumentTable
from DataOperations.MySQL import read_specific_dataframe


class TableCollection:

    def __init__(self, document_category, table_source, metatable=None):
        self.document_category = document_category
        self.table_source = table_source
        self.metatable = metatable

    # Find basic tables from overlap information in meta-table
    def compound_table_from_timeinterval(self, timeinterval, database_connection):
        table_list = self.metatable.find_in_timeinterval(
            timeinterval
        )
        # TODO
        #  - Make general
        #  - Document Group
        table_name = self.metatable.data.loc[table_list[0], "PHOTO_TABLE"]
        table = read_specific_dataframe(
            database_connection,
            table_name,
            self.document_category
        )
        compound_table = DocumentTable(
            table,
            self.document_category,
            table_name
        )
        compound_table = compound_table.data
        for t in table_list[1: ]:
            table_name = self.metatable.data.loc[t, "PHOTO_TABLE"]
            table_new = read_specific_dataframe(
                database_connection,
                table_name,
                self.document_category
            )
            table_new = DocumentTable(
                table_new,
                self.document_category,
                table_name
            )
            # Keeps al columns
            compound_table = pd.concat([
                compound_table,
                table_new.data
            ], ignore_index=True, sort=False)
            # Replace nan by None
            compound_table = compound_table.where(pd.notnull(compound_table), None)
        compound_table = DocumentTable(compound_table, self.document_category)
        compound_table.datetimesort()
        return compound_table