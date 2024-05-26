from DataStructures.TableTypes import table_columns_names_types


class DataTable:
    def __init__(self, table, table_type=None):
        self.table = table
        self.table_type = table_type

    def find_in_timeinterval(self, timeinterval):
        # Returns the index of all documents whose DATE_TIME overlaps a requested time interval
        iix = (self.table["DATE_TIME"] >= timeinterval.left) & (self.table["DATE_TIME"] <= timeinterval.right)
        return DataTable(self.table[iix].reset_index(drop=True))

    def replace_nan(self):
        for col in self.table.columns:
            mysqltype = table_columns_names_types[col]["mysqltype"]
            if mysqltype == "text":
                self.table[col].fillna("", inplace=True)
            elif mysqltype == "integer":
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

