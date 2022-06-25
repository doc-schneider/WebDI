
from DataOperations.Photos import PhotoFactory
from DataOperations.Files import encode_data


# TODO This should be like a parent class to all viewers ?
class Viewer:
    def __init__(self, document_category, document_pathtype, database_connection=None, thumbnail=False):
        self.document_category = document_category
        self.document_pathtype = document_pathtype
        self.database_connection = database_connection
        if document_category == "photo":
            self.encode_type = "base64"
            self.thumbnail = thumbnail

    # Complete file location
    def document_location(self, table):
        # TODO Produces nan instead of None for None + None
        # Absolute file path
        if self.document_pathtype == 'PATH':
            table['LOCATION_DOCUMENT'] = table['PATH'] + table['DOCUMENT_NAME']
            table.loc[table['PATH'] == '', 'LOCATION_DOCUMENT'] = None

    def get_data_type(self, table):
        # TODO Format instead of Type
        if 'DOCUMENT_TYPE' in set(table.columns):
            return table['DOCUMENT_TYPE'].tolist()
        else:
            return list("")

    # Load data from file and return base64 for viewing in website
    def get_data(self, table):
        if self.document_category == "photo":
            self.document_location(table)
            # load and encode_data
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
        elif self.document_category == "browsing":
            # TODO Parent
            return table["LINK"].tolist()

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
        image_names = None  # TODO
        return box_size, image_names