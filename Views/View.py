
from DataOperations.Photos import PhotoFactory
from DataOperations.Evernote import EvernoteFactory
from DataOperations.Files import encode_data


# TODO List of Views better?
class MetaViewer:
    def __init__(self,
                 document_category,
                 document_pathtype,
                 database_connection=None,
                 thumbnail=False
                 ):
        self.document_category = document_category
        self.document_pathtype = document_pathtype
        self.database_connection = database_connection
        self.encode_type = list()
        self.thumbnail = list()
        self.static_basepath = list()
        for d in document_category:
            if d == "photo":
                self.encode_type.append("base64")
                self.thumbnail.append(thumbnail)
                self.static_basepath.append(None)
            elif d == "note":
                self.encode_type.append("html_path")  # TODO Not alwas correct, only for Evernote
                self.thumbnail.append(None)
                self.static_basepath.append(
                    "C:/Users/Stefan/PycharmProjects/WebDI/static/"
                )  # TODO hand over

class Viewer:
    def __init__(self, meta_view, select):
        self.document_category = meta_view.document_category[select]
        self.document_pathtype = meta_view.document_pathtype
        self.database_connection = meta_view.database_connection
        self.encode_type = meta_view.encode_type[select]
        self.thumbnail = meta_view.thumbnail[select]
        self.static_basepath = meta_view.static_basepath[select]

    # Complete file location
    def document_location(self, table):
        # Absolute file path
        if self.document_pathtype == 'PATH':
            table['LOCATION_DOCUMENT'] = table['PATH'] + table['DOCUMENT_NAME']
            table.loc[table['PATH'] == '', 'LOCATION_DOCUMENT'] = None
            # For nan = None + None
            table.loc[table['PATH'].isnull(), 'LOCATION_DOCUMENT'] = None

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
        elif self.encode_type == "html_path":
            EvernoteFactory.copy_html_to_static(table, self.static_basepath)
            # data = path to html source
            return table['STATIC_LOCATION'].tolist()
        elif self.document_category == "browsing":
            # TODO Parent
            return table["LINK"].tolist()

class ViewerFactory:
    # TODO
    #  Separate boostrap form jinja2 properties
    #  Subdivision for timelines, lists, etc

    @staticmethod
    def bootstrap_properties(granularity, time_grid):
        # Boxsizes in the 12 slot schema of bootstrap
        if granularity is None:
            # Single mode. Box size in set in template
            box_size = None
        elif granularity == "10Y":
            box_size = [1 for i in range(10)]
        elif granularity == "Y":
            box_size = [3, 3, 3, 3]  # [2, 2, 2, 2]
            icon_names = ["", "", "", ""]
        elif granularity == "Q":
            box_size = [3, 3, 3]  # [2, 2, 2]
        elif granularity == "M":
            box_size = [2 for i in range(time_grid.shape[0])]
        elif granularity == "W":
            # Small boxes for weekend
            box_size = time_grid["TIME_INTERVAL"].apply(
                lambda x: 1 if x.left.weekday() in [5, 6] else 2
            ).tolist()
        elif granularity == "D":
            box_size = [3 for i in range(4)]  # [2 for i in range(4)]
        elif granularity == "6H":
            box_size = [2 for i in range(6)]
        image_names = None  # TODO
        return box_size, image_names