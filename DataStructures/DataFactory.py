from DataStructures.Data import DataTable
from DataStructures.TableTypes import table_definitions
from DataOperations.MySQL import table_fetch
import config


class DataFactory:
    @staticmethod
    def fetch_table(table_type, table_name):
        table = table_fetch(config.mysql["metadata"], config.mysql["conn"], table_name)
        return DataTable(
            table,
            table_type
        )

# TODO table.drop(columns=table_definitions[table_type]["PrimaryKey"]) ?

