from enum import Enum
from sqlalchemy.types import Text, DateTime, Integer


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
    DOCUMENT = 60
    DOCUMENT_COLLECTION = 70
    EVENT = 80
    MESSAGE = 90
    MESSAGE_COLLECTION = 100
    PERSON = 110

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
}

# TODO AZURE columns
# TODO More columns for ALBUM: eg COLLECTION (eg Stefan's albums), TYPE (classical album, copy of a document)
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
        "ForeignKey": "ID_ALBUM"
    },
    TableType.ALBUM: {
        "Columns": {
            "PHOTO_ALBUM": table_columns_names_types["PHOTO_ALBUM"],
            "DATE_FROM": table_columns_names_types["DATE_FROM"],
            "DATE_TO": table_columns_names_types["DATE_TO"],
            "DESCRIPTION": table_columns_names_types["DESCRIPTION"],
            "OWNER": table_columns_names_types["OWNER"],
        },
        "PrimaryKey": "ID_ALBUM"
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
    TableType.DOCUMENT: {
        "Columns": {
            "FILE_NAME": table_columns_names_types["FILE_NAME"],
            "FILE_FORMAT": table_columns_names_types["FILE_FORMAT"],
            "PATH": table_columns_names_types["PATH"],
            "DATE_TIME": table_columns_names_types["DATE_TIME"],
            "DESCRIPTION": table_columns_names_types["DESCRIPTION"],
            "DOCUMENT_GROUP": table_columns_names_types["DOCUMENT_GROUP"],
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
        "ForeignKey": "ID_MESSAGE_COLLECTION"
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
