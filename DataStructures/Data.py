from DataStructures.TableTypes import table_columns_names_types, table_definitions
from DataOperations.MySQL import table_fetch
import config


class DataTable:
    def __init__(self, table, table_type=None):
        self.table = table
        self.table_type = table_type
    @staticmethod
    def fetch_table(table_type, table_name):
        table = table_fetch(config.mysql["metadata"], config.mysql["conn"], table_name)
        return DataTable(
            table,
            table_type
        )

    def find_in_timeinterval(self, timeinterval):
        # Returns sub-table of all documents whose DATE_TIME overlaps a requested time interval
        iix = (self.table["DATE_TIME"] >= timeinterval.left) & (self.table["DATE_TIME"] <= timeinterval.right)
        return DataTable(self.table[iix].reset_index(drop=True), self.table_type)

    # Return record belonging to a specific foreignkey value
    def match_foreignkey(self, foreignkey_value):
        foreignkey = table_definitions[self.table_type]["ForeignKey"]
        return DataTable(
            self.table.loc[
                self.table[foreignkey] == foreignkey_value, :
            ].reset_index(drop=True),
            self.table_type
        )

    # Add column foreignkey. Get values from foreign table
    def add_foreignkey(self, foreign_column, foreign_table_name):
        foreign_key = table_definitions[self.table_type]["ForeignKey"]
        foreign_table = self.fetch_table(None, foreign_table_name)
        self.table = self.table.merge(
            foreign_table.table[[foreign_column, foreign_key]],
            on=foreign_column,
            how="left"
        )

    def sort(self, column="DATE_TIME"):
        self.table.sort_values(column, ignore_index=True, inplace=True)

    def replace_nan(self):
        for col in self.table.columns:
            mysqltype = table_columns_names_types[col]["mysqltype"]
            if mysqltype == "text":
                self.table[col].fillna("", inplace=True)
            elif mysqltype == "integer":
                #TODO Not so reasonable. However, nan is not accepted by MySQL
                self.table[col].fillna(0, inplace=True)
            elif mysqltype == "datetime":
                pass
                # TODO ?

    def format_path(self):
        # Column PATH
        # type = str
        self.table["PATH"] = self.table["PATH"].astype(str)

    def format_documentgroup(self):
        # Column DOCUMENT_GROUP
        # - type = int
        self.table["DOCUMENT_GROUP"] = self.table["DOCUMENT_GROUP"].astype(int)
        # TODO Roll out DESCRIPTION ect?

