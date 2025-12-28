import pandas as pd

from DataStructures.TableTypes import table_columns_names_types
from DataOperations.MySQL import table_fetch
from DataOperations.Azure import AzureFactory
import config


def fetch_table(table_name):
    if config.environment_storage == "LOCAL":
        table = table_fetch(config.mysql["metadata"], config.mysql["conn"], table_name)
    elif config.environment_storage == "AZURE":
        # TODO Warning setting on copy here ..
        table = AzureFactory.read_table_from_blob("tables", table_name, config.environment_app)
        for col in table.columns:
            if col in table_columns_names_types.keys():
                mysqltype = table_columns_names_types[col]["mysqltype"]
                if mysqltype == "text":
                    table[col] = table[col].astype("string")
                    table[col].fillna("", inplace=True)
                elif mysqltype == "integer":
                    # TODO for null case?
                    pass
                elif mysqltype == "datetime":
                    table[col] = pd.to_datetime(table[col])
                elif mysqltype == "time":
                    # TODO use Helper function
                    table[col] = pd.to_timedelta(table[col])
            else:
                # ID
                # TODO for null case?
                pass
    return table
