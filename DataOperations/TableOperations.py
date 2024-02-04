from DataOperations import MySQL
from DataStructures.TableTypes import TableType, table_types
from DataStructures.TableFactory import DataTableFactory
import config


# Init sqlalchemy table and fetch it from database
def init_table(table_type, person):
    table = {"df": None, "mysql": None, "type": table_type, "name": None}
    table["name"] = person + "_" + table["type"].name.lower()
    # TODO Is the init here necessary (autoload) if the schema is already known in metadata by reflect?
    table["mysql"] = MySQL.init_table(config.mysql["engine"], config.mysql["metadata"], table["name"])
    table["df"] = DataTableFactory.create_table(
        table["type"],
        MySQL.table_fetch(config.mysql["conn"], table["mysql"])
    )
    return table

# Create new table
def create_table(table_type, person, n_rows=None):
    table = {"df": None, "mysql": None, "type": table_type, "name": None}
    table["name"] = person + "_" + table["type"].name.lower()
    if "ParentType" in table_types[table["type"].name].keys():
        parent_table = person + "_" + table_types[table["type"].name]["ParentType"].lower()
    else:
        parent_table = None
    MySQL.create_table(
        config.mysql["engine"],
        config.mysql["metadata"],
        table["name"],
        table["type"],
        parent_table
    )
    table["mysql"] = MySQL.init_table(config.mysql["engine"], config.mysql["metadata"], table["name"])
    table["df"] = DataTableFactory.create_table(table["type"])
    if n_rows:
        # This is not committed to the database. Only dummy for editing in Dash
        table["df"].create_dummy_table(n_rows=n_rows)
    return table


