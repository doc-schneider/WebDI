import sqlite3

from DataOperations.Event import EventTable
from DataOperations.Data import DataTableFactory
from DataOperations.Utilities import timestamplist_to_JSON, JSON_to_timestamplist


class SQLiteFactory:

    @staticmethod
    def map_keytypes(column_name):
        if column_name in ['TIME_FROM', 'TIME_TO']:
            return 'timestamp'