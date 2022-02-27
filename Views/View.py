
from DataOperations.Photos import PhotoFactory
from DataOperations.Files import encode_data


# TODO This should be like a parent class to all viewers ?
class Viewer:
    def __init__(self, document_category, document_pathtype, encode_type='base64', thumbnail=False):
        self.document_category = document_category
        self.document_pathtype = document_pathtype
        self.encode_type = encode_type
        self.thumbnail = thumbnail

    # Complete file location
    def document_location(self, table):
        # Absolute file path
        if self.document_pathtype == 'PATH':
            table['LOCATION_DOCUMENT'] = table['PATH'] + table['DOCUMENT_NAME']
            table.loc[table['PATH'] == '', 'LOCATION_DOCUMENT'] = None

    def get_data_type(self, table):
        return table['DOCUMENT_TYPE'].tolist()

    # Load data from file and return base64 for viewing in website
    def get_data(self, table):
        self.document_location(table)
        # load and encode_data
        if self.document_category == "photo":
            if self.thumbnail:
                return table['LOCATION_DOCUMENT'].apply(
                    PhotoFactory.load_thumbnail,
                    args=(self.encode_type,)
                ).tolist()
            else:
                return table['LOCATION_DOCUMENT'].apply(
                    encode_data,
                    args=(self.encode_type,)
                ).tolist()

    # TODO
    #  Separate boostrap form jinja2 properties
    #  Subdivision for timelines, lists, etc
    def boostrap_properties(self, granularity, time_grid):
        # Boxsizes in the 12 slot schema of bootstrap
        if granularity is None:
            # Single mode. Box size in set in template
            box_size = None
        elif granularity == "10Y":
            box_size = [1 for i in range(10)]
        elif granularity == "Y":
            box_size = [2, 2, 2, 2]
            icon_names = ["", "", "", ""]
        elif granularity == "Q":
            box_size = [2, 2, 2]
        elif granularity == "M":
            box_size = [2 for i in range(time_grid.shape[0])]
        elif granularity == "W":
            # Small boxes for weekend
            box_size = time_grid["TIME_INTERVAL"].apply(
                lambda x: 1 if x.left.weekday() in [5, 6] else 2
            ).tolist()
        elif granularity == "D":
            box_size = [2 for i in range(4)]
        elif granularity == "6H":
            box_size = [2 for i in range(6)]
        image_names = None
        return box_size, image_names