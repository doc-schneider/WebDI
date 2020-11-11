from pathlib import Path

from Views.Parent import ParentViewer
from Views.Utilities import view_data


class StartViewer(ParentViewer):
    def __init__(self, documenttable, document_pathtype, environment):
        super().__init__(n_boxes=1)
        self.encode_type = 'base64'
        self.document_pathtype = document_pathtype
        self.environment = environment
        # Assumes only a single row in table so far
        # photo
        self.index_show = [0]
        self.location_document = self.document_location(documenttable)
        #self.photo_name = documenttable.data['PHOTO_NAME'].iloc[0]
        #self.photo_path = documenttable.data['PHOTO_PATH'].iloc[0]
        #self.photo_azure_container = documenttable.data['PHOTO_AZURE_CONTAINER'].iloc[0]
        #self.photo_azure_blob = documenttable.data['PHOTO_AZURE_BLOB'].iloc[0]
        # bio
        self.first_name = documenttable.data['FIRST_NAME'][0]
        self.family_name = documenttable.data['FAMILY_NAME'][0]
        self.nick_name = documenttable.data['NICK_NAME'][0]
        self.date_birth = documenttable.data['DATE_BIRTH'][0]
        self.description = documenttable.data['DESCRIPTION'][0]
        # Tables to view
        self.document_table = documenttable.data['DOCUMENT_TABLE'].iloc[0]
        self.document_path = documenttable.data['DOCUMENT_PATH'].iloc[0]
        self.document_azure_container = documenttable.data['DOCUMENT_AZURE_CONTAINER'].iloc[0]
        self.document_azure_blob = documenttable.data['DOCUMENT_AZURE_BLOB'].iloc[0]
        self.document_type = documenttable.data['DOCUMENT_TYPE'].iloc[0]
        self.view_type = documenttable.data['VIEW_TYPE'].iloc[0]
        # Event table
        self.event_table = documenttable.data['EVENT_TABLE'].iloc[0]
