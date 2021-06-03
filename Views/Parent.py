#import pandas as pd
#from pathlib import Path

#from DataOperations.Utilities import list_to_str
#from Views.Utilities import view_data, view_text


class Viewer:
    def __init__(self, document_pathtype=None, encode_type=None):
        self.document_pathtype = document_pathtype
        self.encode_type = encode_type



'''
# TODO: Mover more methods here. Move more init here.
class ParentViewer:
    def __init__(self, n_boxes=None, index_documents=list(), document_pathtype='PATH', environment='LOCAL'):
        self.n_boxes = n_boxes    #  Number of viewing boxes on page.
        self.index_documents = index_documents   #  Series of lists, one list for every view box.
        self.index_show = list()     #  Shown document per viewing box
        self.description_document = list()
        self.location_document = list()   #  Locations of shown documents
        self.type_document = list()
        self.encode_type = None     #  Encode type to be sent to webpage
        self.document_pathtype = document_pathtype
        self.environment = environment

    def find_list_column(self, documenttable, column, entry):   #  If column consists of list
        mask = documenttable.data[column].apply(lambda x: entry in x)
        return list(mask[mask==True].index.values)

    def document_location(self, documenttable):
        location_document = list()
        for i in range(self.n_boxes):
            if self.index_show[i] is None:
                location_document.append(None)
            else:
                if self.document_pathtype == 'STATIC_PATH':
                    # Flask static path
                    # TODO Remove Path lib
                    location_document[i] = Path('static/' +
                                                documenttable.data['STATIC_PATH'].iloc[self.index_show[i]] +
                                                '/' +
                                                documenttable.data['DOCUMENT_NAME'].iloc[self.index_show[i]])
                elif self.document_pathtype == 'PATH':
                    # Given absolute path
                    pth = documenttable.data['PATH'].iloc[self.index_show[i]]
                    if not pth:   # Can be None or empty string
                        location_document.append(None)
                    else:
                        location_document.append(pth + '/' +
                                                 documenttable.data['DOCUMENT_NAME'].iloc[self.index_show[i]])
                elif self.document_pathtype == 'AZURE':
                    location_document[i] = [documenttable.data['PATH_AZURE_CONTAINER'].iloc[self.index_show[i]],
                                            documenttable.data['PATH_AZURE_BLOB'].iloc[self.index_show[i]] +
                                            documenttable.data['DOCUMENT_NAME'].iloc[self.index_show[i]]
                                            ]
        return location_document

    def document_type(self, documenttable):
        self.type_document = list()
        for i in range(self.n_boxes):
            if self.index_show[i] is None:
                self.type_document.append(None)
            else:
                # TODO First in list for the time being
                self.type_document.append(
                    documenttable.data['DOCUMENT_TYPE'].iloc[self.index_show[i]][0]
                )

    def document_description(self, documenttable, column):
        description_document = list()
        for i in range(self.n_boxes):
            if self.index_show[i] is None:
                description_document.append('')
            else:
                description_document.append(
                    list_to_str(documenttable.data[column].iloc[self.index_show[i]]))
        return description_document

    # Convert text list object (eg, Description list of an item) to string for website viewing
    # TODO: Enable for other text obects besides Description
    def text_for_view(self):
        list_text = list()
        for ix in self.index_show:
            if ix is None:
                list_text.append(None)
            else:
                list_text.append(view_text(self.description[ix]))
        return list_text

    def data_for_view(self):
        # Produces a list of data of the documents suitable for viewing.
        # TODO: Loop over self.index_show more logical
        list_data = list()
        for i in range(self.n_boxes):
            # Document can only consist of a Description
            if (self.index_show[i] is None) or (self.location_document[i] is None):
                list_data.append(None)
            else:
                data = view_data(self.location_document[i], self.encode_type,
                                 self.document_pathtype, self.environment)
                list_data.append(data)
        return list_data
'''