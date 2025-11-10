import io

from DataStructures.TableTypes import table_columns_names_types, table_definitions, TableType
from DataOperations.Operations_Factory import fetch_table
from DataOperations.Tag import TagFactory


class DataTable:
    def __init__(self, table, table_type=None):
        self.table = table
        self.table_type = table_type

    #TODO Could this be a class method?
    @staticmethod
    def fetch_table(table_type, table_name):
        table = fetch_table(table_name)
        return DataTable(
            table,
            table_type,
        )

    # TODO Files module: Write to local drive?
    # TODO  sep=";" cental defintion?
    def write_table_to_csv(self):
        csv_buffer = io.StringIO()
        self.table.to_csv(csv_buffer, index=False, sep=";")
        csv_buffer.seek(0)  # TODO ?
        return csv_buffer

    def sort(self, column="DATE_TIME"):
        # Second sort with unique ID required since Timestamp can be not unique
        self.table.sort_values(by=[
            column, table_definitions[self.table_type]["PrimaryKey"]
        ], ignore_index=True, inplace=True)

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
    def find_in_timeinterval(self, timeinterval, column="DATE_TIME"):
        # Returns sub-table of all documents whose DATE_TIME overlaps a requested time interval
        iix = (self.table[column] >= timeinterval.left) & (self.table[column] <= timeinterval.right)
        return DataTable(self.table[iix].reset_index(drop=True), self.table_type)

    # Return record belonging to a specific foreignkey value
    def match_foreignkey(self, foreignkey_value, foreignkey=None):
        if not foreignkey:  # In case ForeignKey is a list it needs to be specified
            foreignkey = table_definitions[self.table_type]["ForeignKey"]
        return DataTable(
            self.table.loc[
                self.table[foreignkey] == foreignkey_value, :
            ].reset_index(drop=True),
            self.table_type
        )

    # Add column foreignkey. Get values from foreign table
    # TODO Proper handling of multiple instances of album name
    def add_foreignkey(self, foreign_column, foreign_table_name, foreign_table_type, multiple="last"):
        foreign_table = self.fetch_table(foreign_table_type, foreign_table_name)
        foreign_key = table_definitions[foreign_table_type]["PrimaryKey"]
        foreign_id = foreign_table.table.loc[
            foreign_table.table[foreign_column] == self.table[foreign_column].values[0],
            foreign_key
        ]
        if multiple == "last":
            foreign_id = foreign_id.max()
        else:
            foreign_id = "error"
            print("error")
        self.table[foreign_key] = foreign_id

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



