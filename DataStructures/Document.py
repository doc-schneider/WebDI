from DataStructures.Data import DataTableFactory
from DataStructures.Data import DataTable


# TODO Has this class any distinctive purpose?
class DocumentTable(DataTable):

    def __init__(self, table, document_category, table_name=None):
        super().__init__(table, document_category, table_name)

class DocumentTableFactory:

    # Importing data
    @staticmethod
    def from_csv(document_category, path, filename, parse_date=[]):
        table = DataTableFactory.from_csv(path + filename + ".csv", parse_date)
        return DocumentTable(
            table,
            document_category,
            filename
        )  # TODO Why filename here?


