import pandas as pd

from DataStructures.Document import DocumentTable
from DataOperations.MySQL import read_specific_dataframe
from DataStructures.TableTypes import column_types_table


class TableCollection:

    def __init__(
            self,
            document_category,
            table_source,
            metatable=None,
            category=None,
            tags=None
    ):
        self.document_category = document_category
        self.table_source = table_source
        self.metatable = metatable
        self.category = category
        self.tags = tags

    # Find basic tables from overlap information in meta-table
    def compound_table_from_timeinterval(
            self,
            timeinterval,
            database_connection
    ):
        # Select time interval
        table_list = self.metatable.find_in_timeinterval(
            timeinterval
        )
        # Select Category
        if self.category is not None:
            category_list = self.metatable.data.index[
                self.metatable.data["CATEGORY"] == self.category
            ].to_list()
            table_list = [t for t in table_list if t in category_list]
        # TODO
        #  - Document Group
        columns = column_types_table(
            self.metatable.document_category,
            [],
            remove_primarykey=True,
            return_aliasnames=True
        )
        table_name = self.metatable.data.loc[table_list[0], columns[0]]  # Assume first entry
        table = read_specific_dataframe(
            database_connection,
            table_name,
            self.document_category
        )
        table = self.select_tags(table)
        # Start compound table
        compound_table = DocumentTable(
            table,
            self.document_category,
            table_name
        )
        compound_table = compound_table.data
        # Fill compound table
        for t in table_list[1: ]:
            table_name = self.metatable.data.loc[t, columns[0]]
            table_new = read_specific_dataframe(
                database_connection,
                table_name,
                self.document_category
            )
            table_new = self.select_tags(table_new)
            table_new = DocumentTable(
                table_new,
                self.document_category,
                table_name
            )
            # Keeps all columns
            compound_table = pd.concat([
                compound_table,
                table_new.data
            ], ignore_index=True, sort=False)
            # Replace nan by None
            compound_table = compound_table.where(pd.notnull(compound_table), None)
        compound_table = DocumentTable(compound_table, self.document_category)
        compound_table.datetimesort()
        return compound_table

    def select_tags(self, table):
        # Select tags
        if self.tags is not None:
            return table[table["TAG"].isin(self.tags)]
        else:
            return table