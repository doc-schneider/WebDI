from Views.Parent import ParentViewer


class PlayViewer(ParentViewer):
    def __init__(self):
        super().__init__(n_boxes=1)

    def init_play(self, documenttable, document_pathtype, environment, ix_play):
        self.document_pathtype = document_pathtype
        self.environment = environment
        self.encode_type = 'base64'
        self.index_show = [ix_play]
        self.location_document = self.document_location(documenttable)



