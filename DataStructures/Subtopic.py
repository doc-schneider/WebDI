from DataStructures.Data import DataTable
from DataStructures.TableTypes import TableType


class SubtopicTable(DataTable):

    def __init__(self, table):
        super().__init__(
            table,
            table_type=TableType.SUBTOPIC,
        )
