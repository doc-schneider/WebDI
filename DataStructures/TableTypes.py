from enum import Enum
from sqlalchemy.types import Text, DateTime, Integer, Time


# TODO
#  - FILE table for file operation
# - PHOTO: In a sense of photo album  # TODO Redefine in a sense of general book-like collection
# - ALBUM: Collection of albums / books / CDs .. Like a library
class TableType(Enum):
    PHOTO = 10
    PHOTO_PAGE = 11
    PHOTO_SELECTION = 12
    ALBUM = 20
    ALBUM_SELECTION = 21
    FILM_CONTENT = 24
    FILM = 25
    TAG = 30
    NOTE = 40
    NOTEBOOK = 50
    DOCUMENT = 60
    DOCUMENT_COLLECTION = 70
    EVENT = 80
    MESSAGE = 90
    MESSAGE_COLLECTION = 100
    PERSON = 110
    BIOGRAPHY_SECTION = 120
    BIOGRAPHY = 130

# All column names and their types
# TODO ALBUM instead of PHOTO_ALBUM
table_columns_names_types = {
    "FILE_NAME": {
        "mysqltype": "text",
        "sqlalchemytype": Text
    },
    "FILE_FORMAT": {
        "mysqltype": "text",
        "sqlalchemytype": Text
    },
    "PATH": {
        "mysqltype": "text",
        "sqlalchemytype": Text
    },
    "AZURE_CONTAINER": {
        "mysqltype": "text",
        "sqlalchemytype": Text
    },
    "AZURE_BLOB": {
        "mysqltype": "text",
        "sqlalchemytype": Text
    },
    "DATE_TIME": {
        "mysqltype": "datetime",
        "sqlalchemytype": DateTime
    },
    "DATE_FROM": {
        "mysqltype": "datetime",
        "sqlalchemytype": DateTime
    },
    "DATE_TO": {
        "mysqltype": "datetime",
        "sqlalchemytype": DateTime
    },
    "TIME_FROM": {
        "mysqltype": "time",
        "sqlalchemytype": Time
    },
    "TIME_TO": {
        "mysqltype": "time",
        "sqlalchemytype": Time
    },
    "DESCRIPTION": {
        "mysqltype": "text",
        "sqlalchemytype": Text
    },
    "TEXT": {
        "mysqltype": "text",
        "sqlalchemytype": Text
    },
    "DOCUMENT_GROUP": {
        "mysqltype": "integer",
        "sqlalchemytype": Integer
    },
    "DOCUMENT_ORDER": {
        "mysqltype": "integer",
        "sqlalchemytype": Integer
    },
    "PAGE_NUMBER": {
        "mysqltype": "integer",
        "sqlalchemytype": Integer
    },
    "CHAPTER": {
        "mysqltype": "text",
        "sqlalchemytype": Text
    },
    "PHOTO_ALBUM": {
        "mysqltype": "text",
        "sqlalchemytype": Text
    },
    "PHOTO_ALBUM_SELECTION": {
        "mysqltype": "text",
        "sqlalchemytype": Text
    },
    "BIOGRAPHY": {
        "mysqltype": "text",
        "sqlalchemytype": Text
    },
    "NOTEBOOK": {
        "mysqltype": "text",
        "sqlalchemytype": Text
    },
    "TITLE": {
        "mysqltype": "text",
        "sqlalchemytype": Text
    },
    "ATTACHMENT": {
        "mysqltype": "text",
        "sqlalchemytype": Text
    },
    "NOTEBOOK_COLLECTION": {
        "mysqltype": "text",
        "sqlalchemytype": Text
    },
    "NOTEBOOK_TYPE": {
        "mysqltype": "text",
        "sqlalchemytype": Text
    },
    "DOCUMENT_COLLECTION": {
        "mysqltype": "text",
        "sqlalchemytype": Text
    },
    "MESSAGE_TYPE": {
        "mysqltype": "text",
        "sqlalchemytype": Text
    },
    "SENDER": {
        "mysqltype": "text",
        "sqlalchemytype": Text
    },
    "RECEIVER": {
        "mysqltype": "text",
        "sqlalchemytype": Text
    },
    "MESSAGE_COLLECTION": {
        "mysqltype": "text",
        "sqlalchemytype": Text
    },
    "OWNER": {
        "mysqltype": "text",
        "sqlalchemytype": Text
    },
    "PARTICIPANT": {
        "mysqltype": "text",
        "sqlalchemytype": Text
    },
    "EVENT": {
        "mysqltype": "text",
        "sqlalchemytype": Text
    },
    "PARENT_EVENT": {
        "mysqltype": "text",
        "sqlalchemytype": Text
    },
    "TAG": {
        "mysqltype": "text",
        "sqlalchemytype": Text
    },
    "LOCATION": {
        "mysqltype": "text",
        "sqlalchemytype": Text
    },
    "PERSON": {
        "mysqltype": "text",
        "sqlalchemytype": Text
    },
    "FIRST_NAME": {
        "mysqltype": "text",
        "sqlalchemytype": Text
    },
    "LAST_NAME": {
        "mysqltype": "text",
        "sqlalchemytype": Text
    },
    "CONTENT_TYPE": {
        "mysqltype": "text",
        "sqlalchemytype": Text
    },
}

# TODO AZURE columns
# TODO More columns for ALBUM: eg COLLECTION (eg Stefan's albums), TYPE (classical album)
#
# Tables & Types
table_definitions = {
    TableType.PHOTO: {
        "Columns": {
            "FILE_NAME": table_columns_names_types["FILE_NAME"],
            "FILE_FORMAT": table_columns_names_types["FILE_FORMAT"],
            "PATH": table_columns_names_types["PATH"],
            "DATE_TIME": table_columns_names_types["DATE_TIME"],
            "DESCRIPTION": table_columns_names_types["DESCRIPTION"],
            "DOCUMENT_GROUP": table_columns_names_types["DOCUMENT_GROUP"],
            "PHOTO_ALBUM": table_columns_names_types["PHOTO_ALBUM"],
            "CHAPTER": table_columns_names_types["CHAPTER"],
        },
        "PrimaryKey": "ID_PHOTO",
        "ForeignKey": "ID_ALBUM",
        "ParentTableType": TableType.ALBUM
    },
    TableType.PHOTO_PAGE: {
        "Columns": {
            "FILE_NAME": table_columns_names_types["FILE_NAME"],
            "FILE_FORMAT": table_columns_names_types["FILE_FORMAT"],
            "PATH": table_columns_names_types["PATH"],
            "PAGE_NUMBER": table_columns_names_types["PAGE_NUMBER"],
            "DATE_FROM": table_columns_names_types["DATE_FROM"],
            "DATE_TO": table_columns_names_types["DATE_TO"],
            "DESCRIPTION": table_columns_names_types["DESCRIPTION"],
            "PHOTO_ALBUM": table_columns_names_types["PHOTO_ALBUM"],
            "CHAPTER": table_columns_names_types["CHAPTER"],
        },
        "PrimaryKey": "ID_PHOTO_PAGE",
        "ForeignKey": "ID_ALBUM",
        "ParentTableType": TableType.ALBUM
    },
    TableType.PHOTO_SELECTION: {
        "Columns": {
            "DESCRIPTION": table_columns_names_types["DESCRIPTION"],
            "PHOTO_ALBUM_SELECTION": table_columns_names_types["PHOTO_ALBUM_SELECTION"],
        },
        "PrimaryKey": "ID_PHOTO_SELECTION",
        "ForeignKey": ["ID_PHOTO", "ID_ALBUM_SELECTION"]
    },
    TableType.ALBUM: {
        "Columns": {
            "PHOTO_ALBUM": table_columns_names_types["PHOTO_ALBUM"],
            "CONTENT_TYPE": table_columns_names_types["CONTENT_TYPE"],
            "DATE_FROM": table_columns_names_types["DATE_FROM"],
            "DATE_TO": table_columns_names_types["DATE_TO"],
            "DESCRIPTION": table_columns_names_types["DESCRIPTION"],
            "OWNER": table_columns_names_types["OWNER"],
        },
        "PrimaryKey": "ID_ALBUM"
    },
    TableType.ALBUM_SELECTION: {
        "Columns": {
            "PHOTO_ALBUM_SELECTION": table_columns_names_types["PHOTO_ALBUM_SELECTION"],
            "DATE_FROM": table_columns_names_types["DATE_FROM"],
            "DATE_TO": table_columns_names_types["DATE_TO"],
            "DESCRIPTION": table_columns_names_types["DESCRIPTION"],
            "OWNER": table_columns_names_types["OWNER"],
        },
        "PrimaryKey": "ID_ALBUM_SELECTION"
    },
    TableType.FILM_CONTENT: {
        "Columns": {
            "CHAPTER": table_columns_names_types["CHAPTER"],
            "DATE_FROM": table_columns_names_types["DATE_FROM"],
            "DATE_TO": table_columns_names_types["DATE_TO"],
            "TIME_FROM": table_columns_names_types["TIME_FROM"],
            "TIME_TO": table_columns_names_types["TIME_TO"],
            "DESCRIPTION": table_columns_names_types["DESCRIPTION"],
            "TITLE": table_columns_names_types["TITLE"]
        },
        "PrimaryKey": "ID_FILM_CONTENT",
        "ForeignKey": "ID_FILM",
        "ParentTableType": TableType.FILM
    },
    TableType.FILM: {
        "Columns": {
            "TITLE": table_columns_names_types["TITLE"],
            "FILE_NAME": table_columns_names_types["FILE_NAME"],
            "FILE_FORMAT": table_columns_names_types["FILE_FORMAT"],
            "PATH": table_columns_names_types["PATH"],
            "DATE_FROM": table_columns_names_types["DATE_FROM"],
            "DATE_TO": table_columns_names_types["DATE_TO"],
            "DESCRIPTION": table_columns_names_types["DESCRIPTION"],
            "OWNER": table_columns_names_types["OWNER"],
        },
        "PrimaryKey": "ID_FILM"
    },
    TableType.BIOGRAPHY_SECTION: {
        "Columns": {
            "TITLE": table_columns_names_types["TITLE"],
            "DATE_FROM": table_columns_names_types["DATE_FROM"],
            "DATE_TO": table_columns_names_types["DATE_TO"],
            "CHAPTER": table_columns_names_types["CHAPTER"],
            "BIOGRAPHY": table_columns_names_types["BIOGRAPHY"]
        },
        "PrimaryKey": "ID_BIOGRAPHY_SECTION",
        "ForeignKey": "ID_BIOGRAPHY",
        "ParentTableType": TableType.BIOGRAPHY
    },
    TableType.BIOGRAPHY: {
        "Columns": {
            "BIOGRAPHY": table_columns_names_types["NOTEBOOK"],
            "TITLE": table_columns_names_types["TITLE"],
            "DESCRIPTION": table_columns_names_types["DESCRIPTION"],
            "OWNER": table_columns_names_types["OWNER"],
        },
        "PrimaryKey": "ID_BIOGRAPHY"
    },
    TableType.NOTE: {
        "Columns": {
            "DATE_TIME": table_columns_names_types["DATE_TIME"],
            "TITLE": table_columns_names_types["TITLE"],
            "ATTACHMENT": table_columns_names_types["ATTACHMENT"],
            "NOTEBOOK": table_columns_names_types["NOTEBOOK"],
            "FILE_NAME": table_columns_names_types["FILE_NAME"],
            "FILE_FORMAT": table_columns_names_types["FILE_FORMAT"],
            "PATH": table_columns_names_types["PATH"],
        },
        "PrimaryKey": "ID_NOTE",
        "ForeignKey": "ID_NOTEBOOK",
        "ParentTableType": TableType.NOTEBOOK
    },
    TableType.NOTEBOOK: {
        "Columns": {
            "NOTEBOOK": table_columns_names_types["NOTEBOOK"],
            "NOTEBOOK_COLLECTION": table_columns_names_types["NOTEBOOK_COLLECTION"],
            "NOTEBOOK_TYPE": table_columns_names_types["NOTEBOOK_TYPE"],
            "DATE_FROM": table_columns_names_types["DATE_FROM"],
            "DATE_TO": table_columns_names_types["DATE_TO"],
            "FILE_NAME": table_columns_names_types["FILE_NAME"],
            "FILE_FORMAT": table_columns_names_types["FILE_FORMAT"],
            "PATH": table_columns_names_types["PATH"],
        },
        "PrimaryKey": "ID_NOTEBOOK"
    },
    TableType.DOCUMENT: {
        "Columns": {
            "FILE_NAME": table_columns_names_types["FILE_NAME"],
            "FILE_FORMAT": table_columns_names_types["FILE_FORMAT"],
            "PATH": table_columns_names_types["PATH"],
            "DATE_TIME": table_columns_names_types["DATE_TIME"],
            "DESCRIPTION": table_columns_names_types["DESCRIPTION"],
            "DOCUMENT_GROUP": table_columns_names_types["DOCUMENT_GROUP"],
            "PAGE_NUMBER": table_columns_names_types["PAGE_NUMBER"],
            "DOCUMENT_COLLECTION": table_columns_names_types["DOCUMENT_COLLECTION"],
            "CHAPTER": table_columns_names_types["CHAPTER"],
        },
        "PrimaryKey": "ID_DOCUMENT",
        "ForeignKey": "ID_DOCUMENT_COLLECTION"
    },
    TableType.DOCUMENT_COLLECTION: {
        "Columns": {
            "DOCUMENT_COLLECTION": table_columns_names_types["DOCUMENT_COLLECTION"],
            "DATE_FROM": table_columns_names_types["DATE_FROM"],
            "DATE_TO": table_columns_names_types["DATE_TO"],
            "DESCRIPTION": table_columns_names_types["DESCRIPTION"],
            "OWNER": table_columns_names_types["OWNER"],
        },
        "PrimaryKey": "ID_DOCUMENT_COLLECTION"
    },
    TableType.MESSAGE: {
        "Columns": {
            "MESSAGE_TYPE": table_columns_names_types["MESSAGE_TYPE"],
            "DATE_TIME": table_columns_names_types["DATE_TIME"],
            "SENDER": table_columns_names_types["SENDER"],
            "RECEIVER": table_columns_names_types["RECEIVER"],
            "TEXT": table_columns_names_types["TEXT"],
            "ATTACHMENT": table_columns_names_types["ATTACHMENT"],
            "MESSAGE_COLLECTION": table_columns_names_types["MESSAGE_COLLECTION"],
        },
        "PrimaryKey": "ID_MESSAGE",
        "ForeignKey": "ID_MESSAGE_COLLECTION",
        "ParentTableType": TableType.MESSAGE_COLLECTION
    },
    TableType.MESSAGE_COLLECTION: {
        "Columns": {
            "MESSAGE_COLLECTION": table_columns_names_types["MESSAGE_COLLECTION"],
            "OWNER": table_columns_names_types["OWNER"],
            "PARTICIPANT": table_columns_names_types["PARTICIPANT"],
            "FILE_NAME": table_columns_names_types["FILE_NAME"],
            "FILE_FORMAT": table_columns_names_types["FILE_FORMAT"],
            "PATH": table_columns_names_types["PATH"],
            "DATE_FROM": table_columns_names_types["DATE_FROM"],
            "DATE_TO": table_columns_names_types["DATE_TO"],
            "DESCRIPTION": table_columns_names_types["DESCRIPTION"],
        },
        "PrimaryKey": "ID_MESSAGE_COLLECTION"
    },
    TableType.TAG: {
        "Columns": {
            "TAG": table_columns_names_types["TAG"],
            "DESCRIPTION": table_columns_names_types["DESCRIPTION"],
        },
        "PrimaryKey": "ID_TAG"
    },
    TableType.EVENT: {
        "Columns": {
            "EVENT": table_columns_names_types["EVENT"],
            "DATE_FROM": table_columns_names_types["DATE_FROM"],
            "DATE_TO": table_columns_names_types["DATE_TO"],
            "PARENT_EVENT": table_columns_names_types["PARENT_EVENT"],
            "DESCRIPTION": table_columns_names_types["DESCRIPTION"],
        },
        "PrimaryKey": "ID_EVENT",
        "ForeignKey": "ID_PARENT_EVENT"
    },
    TableType.PERSON: {
        "Columns": {
            "PERSON": table_columns_names_types["PERSON"],
            "FIRST_NAME": table_columns_names_types["FIRST_NAME"],
            "LAST_NAME": table_columns_names_types["LAST_NAME"],
            "DESCRIPTION": table_columns_names_types["DESCRIPTION"],
        },
        "PrimaryKey": "ID_PERSON"
    },
}
