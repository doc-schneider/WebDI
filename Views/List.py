from Views.Parent import ParentViewer
from DataOperations.Utilities import add_thumbnail_to_pathname, add_thumbnail_to_filename


class ListViewer(ParentViewer):
    def __init__(self):
        super().__init__()

    def init_cd_list(self, document_pathtype, environment):
        self.document_pathtype = document_pathtype
        self.environment = environment
        self.encode_type = 'base64'


class ListAllViewer(ListViewer):
    def __init__(self):
        super().__init__()

    def init_cd_list(self, documenttable, document_pathtype, environment, use_thumbnail):
        super().init_cd_list(document_pathtype, environment)

        self.use_thumbnail = use_thumbnail
        # CD cover are documenttable items to be shown
        self.index_show = self.find_list_column(documenttable, 'DESCRIPTION', 'Cover')
        self.n_boxes = len(self.index_show)
        self.location_document = self.document_location(documenttable)
        self.description_document = self.document_description(documenttable, 'PARENT_DESCRIPTION')

        if self.use_thumbnail:
            for i in range(self.n_boxes):
                if self.index_show[i] is not None:
                    if self.document_pathtype == 'AZURE':
                        self.location_document[i][-1] = add_thumbnail_to_filename(self.location_document[i][-1], 'JPG')
                    else:
                        self.location_document[i] = add_thumbnail_to_pathname(self.location_document[i])


class ListSingleViewer(ListViewer):
    def __init__(self):
        super().__init__()

    def init_cd_list(self, documenttable, document_pathtype, environment, ix_cover):
        super().init_cd_list(document_pathtype, environment)

        # TODO: index_documents should be list of lists (but doesn't matter here)
        self.index_documents = self.find_list_column(documenttable, 'PARENT_DESCRIPTION',
                                                documenttable.data['PARENT_DESCRIPTION'].iloc[ix_cover][0])

        self.index_show = self.index_documents.copy()
        self.n_boxes = len(self.index_documents)
        self.description_document = self.document_description(documenttable, 'DESCRIPTION')

        # Ensure that cover is first entry (expected by Jinja)
        ix_cover = self.description_document.index('Cover')
        if ix_cover != 0:
            self.index_documents[0], self.index_documents[ix_cover] = \
                self.index_documents[ix_cover], self.index_documents[0]
            self.index_show = self.index_documents.copy()
            self.description_document = self.document_description(documenttable, 'DESCRIPTION')

        self.location_document = self.document_location(documenttable)

        # Only need to show cover data
        self.index_show[1:] = [None] * (self.n_boxes - 1)


