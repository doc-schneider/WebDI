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
        cols_all = set(
            column_types_table(
                "events",
                optional_columns=[],
                remove_primarykey=True,
                return_aliasnames=True
            )
        )
        table.drop(columns=list(cols - cols_all), inplace=True)
        for c in list(cols_all - cols):
            table[c] = None

        return EventTable(table)

    @staticmethod
    def update_eventtable(events_table_old, events_table):
        # Compares the stored Table with the freshly read table

        # Find new rows based on Event Name
        new_set = set(events_table.data["EVENT_NAME"]) - set(events_table_old["EVENT_NAME"])
        events_new = events_table.data[events_table.data["EVENT_NAME"].isin(new_set)]

        # Old events deleted?
        removed_set = set(events_table_old["EVENT_NAME"]) - (
                set(events_table.data["EVENT_NAME"]) - new_set
        )
        # TODO
        if len(removed_set) > 0:
            pass

        # Existing Events altered?
        # TODO

        return EventTable(events_new.reset_index(drop=True))


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