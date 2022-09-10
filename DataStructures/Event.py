from DataStructures.Data import DataTable


# TODO
#  Distnguish event and events
class EventTable(DataTable):

    def __init__(self, table):
        super().__init__(
            table,
            document_category="events",
            table_name="events"
        )

    def get_events(self, documenttable):
        # Events in EventTable belonging to events in DocumentTable
        events = list(documenttable.data["EVENT"].unique())
        return self.data[self.data["EVENT_NAME"].isin(events)].reset_index(drop=True)

    def find_eventlevel(self, eventlevel):
        return self.data.index[self.data['EVENT_LEVEL'] == eventlevel].to_list()

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

    def create_timeinterval_simple(self):
        # Temporary helper to converting EVENT_TIME (list) to TIME_FROM ..
        self.data['TIME_FROM'] = [t[0] for t in self.data['EVENT_TIME_FROM']]
        self.data['TIME_TO'] = [t[0] for t in self.data['EVENT_TIME_TO']]
