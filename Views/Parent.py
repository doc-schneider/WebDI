import pandas as pd
from pathlib import Path

from DataOperations.Utilities import list_to_str
from Views.Utilities import view_data


class ParentViewer:
    def __init__(self, n_boxes=None, index_documents=list(), document_pathtype='PATH'):
        self.n_boxes = n_boxes    #  Number of viewing boxes on page.
        self.index_documents = index_documents   #  Series of lists, one list for every view box.
        self.index_show = list()     #  Shown document per viewing box
        self.location_document = list()   #  Locations of shown documents
        self.encode_type = None     #  Encode type to be sent to webpage
        self.document_pathtype = document_pathtype

    def find_list_column(self, documenttable, column, entry):   #  If column consists of list
        mask = documenttable.data[column].apply(lambda x: entry in x)
        return list(mask[mask==True].index.values)

    def document_location(self, documenttable):
        location_document = pd.Series([])
        for i in range(self.n_boxes):
            if self.index_show[i] is None:
                location_document[i] = None
            else:
                if self.document_pathtype == 'STATIC_PATH':
                    # Flask static path
                    location_document[i] = Path('static/' +
                                                documenttable.data['STATIC_PATH'].iloc[self.index_show[i]] +
                                                '/' +
                                                documenttable.data['DOCUMENT_NAME'].iloc[self.index_show[i]])
                elif self.document_pathtype == 'PATH':
                    # Given absolute path
                    pth = documenttable.data['PATH'].iloc[self.index_show[i]]
                    if pth is not None:
                        location_document[i] = Path(pth + '/' +
                                                    documenttable.data['DOCUMENT_NAME'].iloc[self.index_show[i]])
                    else:
                        location_document[i] = None
                elif self.document_pathtype == 'AZURE':
                    location_document[i] = [documenttable.data['PATH_AZURE_CONTAINER'].iloc[self.index_show[i]],
                                            documenttable.data['PATH_AZURE_BLOB'].iloc[self.index_show[i]] +
                                            documenttable.data['DOCUMENT_NAME'].iloc[self.index_show[i]]
                                            ]
        return location_document

    def document_description(self, documenttable, column):
        description_document = list()
        for i in range(self.n_boxes):
            if self.index_show[i] is None:
                description_document.append('')
            else:
                description_document.append(list_to_str(documenttable.data[column].iloc[self.index_show[i]],
                                                        column))
        return description_document

    def data_for_view(self):
        # Produces a list of data of the documents suitable for viewing.
        # TODO: Loop over self.index_show more logical
        list_data = list()
        for i in range(self.n_boxes):
            if self.index_show[i] is None:
                list_data.append(None)
            else:
                data = view_data(self.location_document[i], self.encode_type, self.document_pathtype)
                list_data.append(data)
        return list_data