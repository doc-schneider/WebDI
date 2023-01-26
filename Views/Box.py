import pandas as pd


class BoxViewer:
    def __init__(self, View):
        self.View = View
        # TODO Call proper update method

    def update_Timeline(self, documenttable, time_interval):
        self.time_interval = time_interval
        self.index_documents = documenttable.find_in_timeinterval(self.time_interval)
        self.update(documenttable)

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
            "table_name": self.boxShow["TABLE_NAME"].tolist(),
            'data_type': self.View.get_data_type(self.boxShow),  # TODO Format instead of Type
            'data': self.View.get_data(self.boxShow)
        }
        if "EVENT" in self.boxShow.columns:
            dct["event"] = self.boxShow["EVENT"].tolist()
        else:
            dct["event"] = None
        return dct

    # Return list of descriptions
    def get_descriptions(self):
        return self.boxShow['DESCRIPTION'].tolist()

