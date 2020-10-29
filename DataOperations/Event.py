import pandas as pd
import numpy as np

from DataOperations.Data import DataTable


class EventTable(DataTable):

    def __init__(self, table):
        super().__init__(table)

    def add_eventlevel(self):
        # Enhance Event list by an Event level.
        # - Events without Parent Event are level 0
        self.data['EVENT_LEVEL'] = [None] * self.length
        #  No Parent Events
        self.data.loc[self.data['PARENT_EVENT'] == '', 'EVENT_LEVEL'] = 0
        # Repeatedly go through all
        while any(elem is None for elem in self.data['EVENT_LEVEL']):
            for i in range(self.length):
                if self.data['EVENT_LEVEL'].iloc[i] is None:
                    parentEvent = self.data['PARENT_EVENT'].iloc[i]
                    j = self.data.loc[self.data['EVENT_NAME'] == parentEvent].reset_index(
                        drop=True).loc[0, 'EVENT_LEVEL']
                    if j is not None:
                        self.data.loc[i, 'EVENT_LEVEL'] = j + 1

    # Get parent events for event series
    def get_ParentEvent(self, eventNames):
        parent_events = []
        for e in eventNames:
            if e is not None:
                parent_events.append(self.data['PARENT_EVENT'].loc[self.data['EVENT_NAME']==e].
                                     to_list()[0])
            else:
                parent_events.append(None)
        return parent_events


class EventFactory:

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