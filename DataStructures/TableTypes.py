from enum import Enum
from sqlalchemy.types import Text, DateTime, Date, Integer, Boolean


class TableType(Enum):
    TOPIC = 0
    SUBTOPIC = 1
    BOOKLIST = 2


# Re-usable Names and their Type
#
columns_names_types = {
    "NAME":{
        "mysqltype": "text",
        "sqlalchemytype": Text
    },
    "DESCRIPTION":{
        "mysqltype": "text",
        "sqlalchemytype": Text
    },
    "PATH":{
        "mysqltype": "text",
        "sqlalchemytype": Text
    }
}

# Tables & Types
#
table_types = {
    TableType.TOPIC.name: {
        "Columns": {
            "TOPIC": {
                "mysqltype": "text",
                "sqlalchemytype": Text
            },
            "DESCRIPTION": columns_names_types["DESCRIPTION"],
        },
        "PrimaryKey": "ID_TOPIC"
    },
    TableType.SUBTOPIC.name: {
        "Columns": {
            "SUBTOPIC": {
                "mysqltype": "text",
                "sqlalchemytype": Text
            },
            "PATH": columns_names_types["PATH"],
            "DESCRIPTION": columns_names_types["DESCRIPTION"],
        },
        "PrimaryKey": "ID_SUBTOPIC",
        "ForeignKey": "ID_TOPIC",
        "ParentType": TableType.TOPIC.name
    },
    TableType.BOOKLIST.name: {
        "Columns":{
        "NAME":  columns_names_types["NAME"],
        "DESCRIPTION": columns_names_types["DESCRIPTION"],
        "PATH": columns_names_types["PATH"],
        "BELONGS_TO":{
            "mysqltype": "text",
            "sqlalchemytype": Text
        },
        "YEAR_PUBLISHED":{
            "mysqltype": "integer",
            "sqlalchemytype": Integer
        }
    },
    "PrimaryKey": "ID_Booklist"
    }
}

