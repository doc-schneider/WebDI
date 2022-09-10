import pandas as pd

from DataStructures.Event import EventTable
from DataStructures.TableTypes import column_types_table


class EventFactory:

    @staticmethod
    def table_from_csv(
            path_table
    ):
        table = pd.read_csv(
            path_table,
            encoding='ANSI',
            sep=';',
            parse_dates=["TIME_FROM", "TIME_TO"],
            dayfirst=True
        )
        # Replace nan by None
        table = table.where(pd.notnull(table), None)

        # Remove non-defined columns
        cols = set(table.columns)
        dct = column_types_table("events")
        dct.pop("primary_key")
        cols_all = set([value["alias"] for (key, value) in dct.items()])
        table.drop(columns=list(cols - cols_all), inplace=True)
        for c in list(cols_all - cols):
            table[c] = None

        return EventTable(table)

'''
    @staticmethod
    def extract_event_from_table(table):
        # Extracts event name and time span from a DocumentTable (eg, while DocumentTable is
        # constructed by means of a pre-table)
        event_name = np.unique(table.data['EVENT'].values)[0]  # Assume single event for all for the time being
        table.timesort()   # Earliest Time_From
        time_from = table.data['TIME_FROM'].iloc[0]
        table.data.sort_values(by=['TIME_TO'], inplace=True)
        table.data.reset_index(drop=True, inplace=True)
        time_to = table.data['TIME_TO'].iloc[-1]
        # TODO : EventLevel?
        df = pd.DataFrame({'TIME_FROM': [time_from], 'TIME_TO': [time_to], 'EVENT_NAME': [event_name],
                           'PARENT_EVENT': [None]})  # One line EventTable
        return EventTable(df)

    @staticmethod
    def append_to_eventtable(column_name):    # String items can appear in lists in these columns.
        return column_name in ['DESCRIPTION', 'PARENT_DESCRIPTION', 'CATEGORY', 'PARENT_CATEGORY']
'''