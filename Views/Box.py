import pandas as pd

from DataStructures.Data import DataTable
from Views.Timeline_Factory import TimelineFactory


class BoxViewer:
    def __init__(self, View):
        self.View = View
        # TODO Call proper update method

    def update_Timeline(self, documenttable, eventtable, time_interval):
        self.time_interval = time_interval
        self.index_documents = documenttable.find_in_timeinterval(self.time_interval)[0]

        self.update(documenttable)

        # Add Event information to Show document
        self.event = {
            "event_marker": None,
            "event_name": None,
            "event_description": None
        }
        events = eventtable.get_events(
            DataTable(self.boxShow)
        )
        if not events.empty:
            self.event["event_name"] = events["EVENT_NAME"].values[0]
            self.event["event_description"] = events["DESCRIPTION"].values[0]
            # Graphics
            self.event["event_marker"] = TimelineFactory.position_width(
                events.loc[0, ["TIME_FROM", "TIME_TO"]],
                time_interval
            )

    # General update method for BoxView
    def update(self, documenttable, shift_show=None):
        # Grouping of documents in one Box?
        if 'GROUP_INDEX' in documenttable.data:
            self.index_groups = documenttable.data.loc[
                self.index_documents, 'GROUP_INDEX'
            ].unique().tolist()
        else:
            self.index_groups = None
        # Select the one to show
        # TODO Generalize to lists etc
        self.select_show(shift_show)
        # Dataframe holding the current document to show
        if self.index_show is not None:
            if self.index_groups:
                self.boxShow = documenttable.data.loc[
                    documenttable.data['GROUP_INDEX']==self.index_show,
                ].copy()
            else:
                self.boxShow = documenttable.data.loc[[self.index_show], ].copy()
        else:
            # empty box
            # TODO : "" empty str?
            self.boxShow = pd.DataFrame({x: [None] for x in documenttable.data.columns})
        # How many subboxes for a group?
        self.n_subboxes = self.boxShow.shape[0]

    # Which document to show in box.
    # - Initial Default: first.
    # - Shift: + / - 1
    # TODO Extend to lists etc
    def select_show(self, shift_show=None):
        if shift_show is None:
            # Initial
            self.index_show = None
            which = 0
        else:
            if self.index_groups is not None:
                # TODO
                pass
            else:
                n = len(self.index_documents)
                which = self.index_documents.index(self.index_show)
            which += shift_show
            which = max(0, min(which, n-1))
        if self.index_groups is not None:
            if self.index_groups:
                self.index_show = self.index_groups[which]
        else:
            if self.index_documents:
                self.index_show = self.index_documents[which]

    # For Jinja
    def view(self):
        # TODO Look up components in Table Type
        dct = {
            'n_subboxes': self.n_subboxes,
            "category": self.View.document_category,
            'description': self.get_descriptions(),
            "table_name": self.boxShow["NAME_TABLE"].values[0],
            'data_format': self.View.get_data_format(self.boxShow),
            'data': self.View.get_data(self.boxShow),
            "event_name": self.event["event_name"],  # TODO Doesn't work for non-timeline
            "event_description": self.event["event_description"],
            "event_marker": self.event["event_marker"]
        }
        if "TAG" in self.boxShow.columns:
            dct["tag"] = self.boxShow["TAG"].tolist()
        else:
            dct["tag"] = None
        return dct

    # Return list of descriptions
    def get_descriptions(self):
        return self.boxShow['DESCRIPTION'].tolist()

