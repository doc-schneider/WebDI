from Views.Parent import ParentViewer
from Views.Utilities import timegrid, find_documents, show_documents, \
    graphics_markers_time, find_events
from DataOperations.Utilities import add_thumbnail_to_pathname


class TimelineViewer(ParentViewer):
    def __init__(self, n_boxes):
        super().__init__(n_boxes)

    def init_photo_timeline(self, document_pathtype):
        self.document_pathtype = document_pathtype
        self.encode_type = 'base64'


class TimelineAllViewer(TimelineViewer):
    def __init__(self, n_boxes):
        super().__init__(n_boxes)

    def init_photo_timeline(self, documenttable, document_pathtype, use_thumbnail, eventtable,
                            start_interval=None):
        super().init_photo_timeline(document_pathtype)
        self.use_thumbnail = use_thumbnail
        if start_interval is None:
            # Use documenttable as time interval default.
            self.timegrid = timegrid(documenttable.data['TIME_FROM'].iloc[0],
                                     documenttable.data['TIME_TO'].iloc[-1], self.n_boxes)
        else:
            self.timegrid = timegrid(start_interval[0], start_interval[1], self.n_boxes)
        self.events = find_events(eventtable, documenttable)
        self.update(documenttable)

    def update(self, documenttable):
        self.index_documents = find_documents(documenttable, self.timegrid)
        self.index_show = show_documents(self.index_documents)
        self.location_document = self.document_location(documenttable)
        self.description_document = self.document_description(documenttable, 'DESCRIPTION')

        if self.use_thumbnail:
            for i in range(self.n_boxes):
                if self.index_show[i] is not None:
                    self.location_document[i] = add_thumbnail_to_pathname(self.location_document[i])

        # Document occurrence timeline
        self.markers_time_documents = graphics_markers_time(documenttable.data, self.index_documents,
                                                            (self.timegrid['TIME_FROM'].iloc[0],
                                                             self.timegrid['TIME_TO'].iloc[-1]))
        # Event timeline
        ix = list(range(0,self.events.shape[0]))
        self.markers_time_events = graphics_markers_time(self.events, [ix],
                                                            (self.timegrid['TIME_FROM'].iloc[0],
                                                             self.timegrid['TIME_TO'].iloc[-1]))
        self.labels_time_events = [self.events['EVENT_NAME'].iloc[0],
                                   self.markers_time_events[0][0]]  # Left edge of label = leftmost event time
        #graphics_event_label()

    def earlier(self, documenttable):
        # Shift one block
        t_start = self.timegrid['TIME_FROM'].iloc[0]
        t_end = self.timegrid['TIME_TO'].iloc[-1]
        time_delta = (t_end - t_start) / self.n_boxes
        t_start = t_start - time_delta
        t_end = t_end - time_delta
        self.timegrid = timegrid(t_start, t_end, self.n_boxes)
        self.update(documenttable)

    def later(self, documenttable):
        # Shift one block
        t_start = self.timegrid['TIME_FROM'].iloc[0]
        t_end = self.timegrid['TIME_TO'].iloc[-1]
        time_delta = (t_end - t_start) / self.n_boxes
        t_start = t_start + time_delta
        t_end = t_end + time_delta
        self.timegrid = timegrid(t_start, t_end, self.n_boxes)
        self.update(documenttable)

    def zoom_in(self, documenttable):
        # Make 2 middle blocks new total time interval
        t_start = self.timegrid['TIME_FROM'].iloc[2]   # TODO: make general
        t_end = self.timegrid['TIME_TO'].iloc[3]
        self.timegrid = timegrid(t_start, t_end, self.n_boxes)
        self.update(documenttable)

    def zoom_out(self, documenttable):
        # Make all blocks into the 2 middle blocks
        t_1 = self.timegrid['TIME_FROM'].iloc[0]
        t_2 = self.timegrid['TIME_TO'].iloc[-1]
        t_start = t_1 - (t_2 - t_1)  # 2 blocks to start   # TODO: make general
        t_end = t_2 + (t_2 - t_1)
        self.timegrid = timegrid(t_start, t_end, self.n_boxes)
        self.update(documenttable)


# Single frame view on documents within one time interval (index_documents)
class TimelineSingleViewer(TimelineViewer):
    def __init__(self):
        super().__init__(n_boxes=1)

    def init_photo_timeline(self, documenttable, document_pathtype, index_documents, index_show):
        super().init_photo_timeline(document_pathtype)
        self.index_documents = index_documents
        self.index_show = [index_show]
        self.index = 0    # Initially show first document
        self.n_documents = len(index_documents)
        self.timegrid = timegrid(documenttable.data['TIME_FROM'].iloc[self.index_documents[0]],
                                 documenttable.data['TIME_TO'].iloc[self.index_documents[-1]], 1)
        self.markers_time_documents = graphics_markers_time(documenttable.data, [self.index_documents],
                                                            (self.timegrid['TIME_FROM'].iloc[0],
                                                             self.timegrid['TIME_TO'].iloc[-1]))
        self.update(documenttable)

    def update(self, documenttable):
        self.location_document = self.document_location(documenttable)
        self.description_document = self.document_description(documenttable, 'DESCRIPTION')
        # Emphasize mark for currently viewed document
        self.markers_time_show = graphics_markers_time(documenttable.data, [self.index_show],
                                                            (self.timegrid['TIME_FROM'].iloc[0],
                                                             self.timegrid['TIME_TO'].iloc[-1]))

    def earlier(self, documenttable):
        # Shift one
        if self.index > 0:
            self.index = self.index - 1
            self.index_show = [self.index_documents[self.index]]
        self.update(documenttable)

    def later(self, documenttable):
        if self.index < self.n_documents - 1:
            self.index = self.index + 1
            self.index_show = [self.index_documents[self.index]]
        self.update(documenttable)


'''

class FrameViewer(ParentViewer):
    def __init__(self, documenttable, eventtable, t_start, t_end, viewtype, document_pathtype,
                 index_documents):
        super().__init__(documenttable, eventtable, t_start, t_end, viewtype, document_pathtype,
                         index_documents)
        self.n_boxes = 1
        self.index = 0    # Initially show first document
        self.index_show = [index_documents[0]]
        self.n_documents = len(index_documents)
        self.location_document = self.document_location(documenttable)
        self.description_document = self.document_description(documenttable)
        self.timeinterval_document = documenttable.data['TIME_INTERVAL'].loc[self.index_show[0]]
        self.event_document = documenttable.data['EVENT'].loc[self.index_show[0]]
        #self.event_parent = eventtable.get_ParentEvent(self.event_document)

    def update(self, documenttable, eventtable):
        self.location_document = self.document_location(documenttable)
        self.description_document = self.document_description(documenttable)
        self.timeinterval_document = documenttable.data['TIME_INTERVAL'].loc[self.index_show[0]]
        self.event_document = documenttable.data['EVENT'].loc[self.index_show[0]]
        #self.event_parent = eventtable.get_ParentEvent(self.event_document)

'''