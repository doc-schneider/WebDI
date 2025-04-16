from pathlib import Path
import pandas as pd
import io

from DataStructures.TableTypes import table_columns_names_types, table_definitions
from DataOperations.MySQL import table_fetch
from DataOperations.Azure import AzureFactory
from DataOperations.Tag import TagFactory
import config


class DataTable:
    def __init__(self, table, table_type=None):
        self.table = table
        self.table_type = table_type

    #TODO Could this be a class method?
    @staticmethod
    def fetch_table(table_type, table_name):
        if config.environment_storage == "LOCAL":
            table = table_fetch(config.mysql["metadata"], config.mysql["conn"], table_name)
        elif config.environment_storage == "AZURE":
            table = AzureFactory.read_table_from_blob("tables", table_name + ".csv", config.environment_app)
            for col in table.columns:
                if col in table_columns_names_types.keys():
                    mysqltype = table_columns_names_types[col]["mysqltype"]
                    if mysqltype == "text":
                        table[col] = table[col].astype(str)
                        table[col].fillna("", inplace=True)
                    elif mysqltype == "integer":
                        pass
                        # TODO for null case
                    elif mysqltype == "datetime":
                        table[col] = pd.to_datetime(table[col])
                else:
                    # ID
                    # TODO for null case?
                    pass
        return DataTable(
            table,
            table_type
        )

    # TODO Into Files module?
    # TODO Too complicated. Do direct creation, not buffer
    def write_table_to_csv(self):
        csv_buffer = io.StringIO()
        self.table.to_csv(csv_buffer, index=False, sep=";")
        csv_buffer.seek(0)
        return csv_buffer

    def sort(self, column="DATE_TIME"):
        self.table.sort_values(column, ignore_index=True, inplace=True)

    def filter(self, filter_table=[{}]):
        if filter_table:
            if "TAG" in filter_table.keys():
                tag = filter_table.pop("TAG")
                # Find rows in TAG column containing tag
                if "TAG" in self.table.columns:
                    tag_series = self.table["TAG"].apply(lambda x: TagFactory.process_tags(x))
                    table = self.table[tag_series.apply(lambda x: tag in x)].reset_index(drop=True)
                else:
                    table = self.table
            else:
                table = self.table
            # Normal columns
            filtered_dict = {key: value for key, value in filter_table.items() if key in self.table.columns}
            if filtered_dict:
                query_str = ' & '.join([f'{k} == @{k}' for k in filtered_dict.keys()])
                table = table.query(query_str, local_dict=filter_table).reset_index(drop=True)
        else:
            table = self.table
        return DataTable(
            table,
            self.table_type
        )

    #TODO Separate function for converting TAG column to lists?

    #TODO Do exclusive right boundary
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

    # TODO These should possibly located in MySQL. In memory / DataFrame should store them as Path etc
    #
    # Can't I upload "null" to MySql ?
    def replace_nan(self):
        for col in self.table.columns:
            mysqltype = table_columns_names_types[col]["mysqltype"]
            if mysqltype == "text":
                self.table[col].fillna("", inplace=True)
            elif mysqltype == "integer":
                #TODO Not so reasonable. However, nan is not accepted by MySQL?
                self.table[col].fillna(0, inplace=True)
            elif mysqltype == "datetime":
                pass
                # TODO ?
    #
    def format_path(self, cols=["PATH"]):
        # type = str
        for col in cols:
            self.table[col] = self.table[col].astype(str)
    #
    def format_documentgroup(self):
        # Column DOCUMENT_GROUP
        # - type = int
        self.table["DOCUMENT_GROUP"] = self.table["DOCUMENT_GROUP"].astype(int)
        # TODO Roll out DESCRIPTION ect?



