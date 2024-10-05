from enum import Enum
from sqlalchemy.types import Text, DateTime, Date, Integer, Boolean


# TODO
#  - FILE table for file operation
# - PHOTO: In a sense of photo album  # TODO Redefine in a sense of general book-like collection
# - ALBUM: Collection of albums / books / CDs .. Like a library
class TableType(Enum):
    PHOTO = 10
    ALBUM = 20
    TAG = 30
    NOTE = 40
    NOTEBOOK = 50

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
    "DESCRIPTION": {
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
    "PHOTO_ALBUM": {
        "mysqltype": "text",
        "sqlalchemytype": Text
    },
    "CHAPTER": {
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
    "EVENT": {
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
}

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
        "ForeignKey": "ID_ALBUM"
    },
    TableType.ALBUM: {
        "Columns": {
            "PHOTO_ALBUM": table_columns_names_types["PHOTO_ALBUM"],
            "DATE_FROM": table_columns_names_types["DATE_FROM"],
            "DATE_TO": table_columns_names_types["DATE_TO"],
            "DESCRIPTION": table_columns_names_types["DESCRIPTION"],
        },
        "PrimaryKey": "ID_ALBUM"
    },
    TableType.TAG: {
        "Columns": {
            "TAG": table_columns_names_types["TAG"],
            "DESCRIPTION": table_columns_names_types["DESCRIPTION"],
        },
        "PrimaryKey": "ID_TAG"
    },
    TableType.NOTE: {
        "Columns": {
            "FILE_NAME": table_columns_names_types["FILE_NAME"],
            "FILE_FORMAT": table_columns_names_types["FILE_FORMAT"],
            "PATH": table_columns_names_types["PATH"],
            "DATE_TIME": table_columns_names_types["DATE_TIME"],
            "TITLE": table_columns_names_types["TITLE"],
            "ATTACHMENT": table_columns_names_types["ATTACHMENT"],
            "NOTEBOOK": table_columns_names_types["NOTEBOOK"],
        },
        "PrimaryKey": "ID_NOTE",
        "ForeignKey": "ID_NOTEBOOK"
    },
    TableType.NOTEBOOK: {
        "Columns": {
            "NOTEBOOK": table_columns_names_types["NOTEBOOK"],
            "NOTEBOOK_COLLECTION": table_columns_names_types["NOTEBOOK_COLLECTION"],
            "NOTEBOOK_TYPE": table_columns_names_types["NOTEBOOK_TYPE"],
            "DATE_FROM": table_columns_names_types["DATE_FROM"],
            "DATE_TO": table_columns_names_types["DATE_TO"],
        },
        "PrimaryKey": "ID_NOTEBOOK"
    },
}
