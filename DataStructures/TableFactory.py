import pandas as pd

from DataStructures.Topic import TopicTable
from DataStructures.Subtopic import SubtopicTable

# Acts as a distributor to the various Table classes

class DataTableFactory:
    @staticmethod
    def create_table(table_type, df=None):
        if table_type.name == "TOPIC":
            return TopicTable(df)
        if table_type.name == "SUBTOPIC":
            return SubtopicTable(df)

    # TODO Type missing?
    # Importing data
    @staticmethod
    def from_csv(file, parse_date=[]):
        table = pd.read_csv(
            file,
            encoding='ANSI',
            sep=';',
            parse_dates=parse_date,
            dayfirst=True
        )
        table = table.where(pd.notnull(table), None)
        return table

