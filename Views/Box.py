import pandas as pd

#from DataOperations.Utilities import add_thumbnail_to_filename
#from Views.Utilities import list_column_to_str
from DataOperations.Photos import PhotoFactory
from DataOperations.Files import encode_data


class BoxViewer():
    def __init__(self, View):
        self.View = View

    # photoTimeline specifics: Time, photo information
    def init_photoTimeline(self, use_thumbnail):
        self.use_thumbnail = use_thumbnail

    def update_photoTimeline(self, documenttable, time_interval):
        self.timeinterval = pd.Interval(time_interval['TIME_FROM'],
                                   time_interval['TIME_TO'], closed='left')
        self.index_documents = documenttable.find_in_timeinterval(self.timeinterval)
        self.update(documenttable)

    # General update method for BoxView
    def update(self, documenttable, shift_show=None):
        if 'GROUP_INDEX' in documenttable.data:
            self.index_groups = documenttable.data.loc[self.index_documents, 'GROUP_INDEX'].unique().tolist()
        else:
            self.index_groups = None
        self.select_show(shift_show)
        # TODO Define empty box
        # Dataframe holding the current document to show
        if self.index_show is not None:
            if self.index_groups:
                self.boxShow = \
                    documenttable.data.loc[documenttable.data['GROUP_INDEX']==self.index_show, ].copy()
            else:
                self.boxShow = documenttable.data.loc[[self.index_show], ].copy()
        else:  # empty box
            self.boxShow = self.empty_box()
        self.n_subboxes = self.boxShow.shape[0]
        self.document_location()
        # # Convert lists to string or None
        #self.boxShow['DOCUMENT_TYPE'] = self.boxShow['DOCUMENT_TYPE'].apply(list_column_to_str)
        #self.boxShow['DESCRIPTION'] = self.boxShow['DESCRIPTION'].apply(list_column_to_str)

    # Which document to show in box.
    # - Initial Default: first.
    # - Shift: + / - 1
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
            which = max(0, min(which, n))

        if self.index_groups is not None:
            if self.index_groups:
                self.index_show = self.index_groups[which]
        else:
            if self.index_documents:
                self.index_show = self.index_documents[which]

    # Complete file location
    def document_location(self):
        # Absolute file path
        if self.View.document_pathtype == 'PATH':
            self.boxShow['LOCATION_DOCUMENT'] = self.boxShow['PATH'] + '/' + self.boxShow['DOCUMENT_NAME']
            self.boxShow.loc[self.boxShow['PATH']=='', 'LOCATION_DOCUMENT'] = None

    # Empty box
    def empty_box(self):
        return pd.DataFrame({'PATH': [''], 'DOCUMENT_NAME': [''], 'DOCUMENT_TYPE': [''],
                             'DESCRIPTION': ['']})  # Lists ..

    ## Methods for website viewing

    # Return list of descriptions
    def descriptions(self):
        return self.boxShow['DESCRIPTION'].tolist()

    def document_type(self):
        return self.boxShow['DOCUMENT_TYPE'].tolist()

    # Load data from file and return base64 for viewing in website
    def get_data(self):
        # load and encode_data
        if self.use_thumbnail:
            return self.boxShow['LOCATION_DOCUMENT'].apply(
                PhotoFactory.load_thumbnail,
                args=(self.View.encode_type,)
            ).tolist()
        else:
            return self.boxShow['LOCATION_DOCUMENT'].apply(
                encode_data,
                args=(self.View.encode_type,)
            ).tolist()
