
from DataOperations.Photos import PhotoFactory
from DataOperations.Files import encode_data


# TODO This should be like a parent class to all viewers
#  - Could be concerned with processing data into viewable format and other methods
class Viewer:
    def __init__(self, document_category, document_pathtype, encode_type, thumbnail=False):
        self.document_category = document_category
        self.document_pathtype = document_pathtype
        self.encode_type = encode_type
        self.thumbnail = thumbnail

    # Complete file location
    def document_location(self, table):
        # Absolute file path
        if self.document_pathtype == 'PATH':
            table['LOCATION_DOCUMENT'] = table['PATH'] + '/' + table['DOCUMENT_NAME']
            table.loc[table['PATH'] == '', 'LOCATION_DOCUMENT'] = None

    def get_data_type(self, table):
        return table['DOCUMENT_TYPE'].tolist()

    # Load data from file and return base64 for viewing in website
    def get_data(self, table):
        self.document_location(table)
        # load and encode_data
        if self.document_category == "photo":
            if self.use_thumbnail:
                return table['LOCATION_DOCUMENT'].apply(
                    PhotoFactory.load_thumbnail,
                    args=(self.View.encode_type,)
                ).tolist()
            else:
                pass
                #return self.boxShow['LOCATION_DOCUMENT'].apply(
                #    encode_data,
                #    args=(self.View.encode_type,)
                #).tolist()
