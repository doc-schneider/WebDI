from enum import Enum
from sqlalchemy.types import Text, DateTime, Date, Integer, Boolean


class TableType(Enum):
    PHOTO = 10

# All column names and their types
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
    "DESCRIPTION": {
        "mysqltype": "text",
        "sqlalchemytype": Text
    },
    "DOCUMENT_GROUP": {
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
}

# Tables & Types
table_types = {
    TableType.PHOTO: {
        "Columns": {
            "FILE_NAME": table_columns_names_types["FILE_NAME"],
            "FILE_FORMAT": table_columns_names_types["FILE_FORMAT"],
            "PATH": table_columns_names_types["PATH"],
            "DESCRIPTION": table_columns_names_types["DESCRIPTION"],
            "DOCUMENT_GROUP": table_columns_names_types["DOCUMENT_GROUP"],
            "PHOTO_ALBUM": table_columns_names_types["PHOTO_ALBUM"],
            "CHAPTER": table_columns_names_types["CHAPTER"],
        },
        "PrimaryKey": "ID_PHOTO"
    },
}
