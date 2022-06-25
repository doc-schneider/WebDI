from sqlalchemy import Text, DateTime, Date, Integer


# TODO What makes sense?
# Common to all table types
columns_common = {
    "Description": {
        "mysqltype": "text",
        "sqlalchemytype": Text,
        "alias": "DESCRIPTION"
    },
    "Tag": {
        "mysqltype": "text",
        "sqlalchemytype": Text,
        "alias": "TAG"
    },
    "TableName": {
        "mysqltype": "text",
        "sqlalchemytype": Text,
        "alias": "TABLE_NAME"
    }
}

columns_optional = {
    "DocumentGroup": {
        "mysqltype": "integer",
        "sqlalchemytype": Integer,
        "alias": "DOCUMENT_GROUP"
    },
    "Location": {
        "mysqltype": "text",
        "sqlalchemytype": Text,
        "alias": "LOCATION"
    }
}

# Meta table for photos table
columns_photostable = {
    "PhotoTable": {
        "mysqltype": "text",
        "sqlalchemytype": Text,
        "alias": "PHOTO_TABLE"
    },
    "TimeFrom": {
        "mysqltype": "datetime",
        "sqlalchemytype": DateTime,
        "alias": "TIME_FROM"
    },
    "TimeTo": {
        "mysqltype": "datetime",
        "sqlalchemytype": DateTime,
        "alias": "TIME_TO"
    },
    "primary_key": "PhotosID"
}

# TODO
#  - PhotosID?
columns_phototable = {
    "PhotoName": {
        "mysqltype": "text",
        "sqlalchemytype": Text,
        "alias": "DOCUMENT_NAME"
    },
    "PhotoType": {   # TODO Should be "Format"
        "mysqltype": "text",
        "sqlalchemytype": Text,
        "alias": "DOCUMENT_TYPE"
    },
    "DateTime": {
        "mysqltype": "datetime",
        "sqlalchemytype": DateTime,
        "alias": "DATETIME"
    },
    "Path": {
        "mysqltype": "text",
        "sqlalchemytype": Text,
        "alias": "PATH"
    },
    "Event": {                    # TODO Should not be part of the core photo table. Optional?
        "mysqltype": "text",
        "sqlalchemytype": Text,
        "alias": "EVENT"
    },
    "primary_key": "PhotoID"
}

columns_browsingtable = {
    "DateTime": {
        "mysqltype": "datetime",
        "sqlalchemytype": DateTime,
        "alias": "DATETIME"
    },
    "Link": {
        "mysqltype": "text",
        "sqlalchemytype": Text,
        "alias": "LINK"
    },
    "Parent": {
        "mysqltype": "text",
        "sqlalchemytype": Text,
        "alias": "PARENT"
    },
    "Event": {                        # TODO Remove
        "mysqltype": "text",
        "sqlalchemytype": Text,
        "alias": "EVENT"
    },
    "primary_key": "BrowsingID"
}

columns_eventsstable = {
    "EventName": {
        "mysqltype": "text",
        "sqlalchemytype": Text,
        "alias": "EVENT_NAME"
    },
    "TimeFrom": {
        "mysqltype": "datetime",
        "sqlalchemytype": DateTime,
        "alias": "TIME_FROM"
    },
    "TimeTo": {
        "mysqltype": "datetime",
        "sqlalchemytype": DateTime,
        "alias": "TIME_TO"
    },
    "ParentEvent": {
        "mysqltype": "text",
        "sqlalchemytype": Text,
        "alias": "PARENT_EVENT"
    },
    "ParentEventId": {
        "mysqltype": "integer",
        "sqlalchemytype": Integer,
        "alias": "PARENT_EVENT_ID"
    },
    "primary_key": "EventID"
}

# Meta table for books
# Links to Pages table
# DateCreated: Time created
columns_bookstable = {
    "DocumentName": {
        "mysqltype": "text",
        "sqlalchemytype": Text,
        "alias": "DOCUMENT_NAME"
    },
    "BookTable": {
        "mysqltype": "text",
        "sqlalchemytype": Text,
        "alias": "BOOK_TABLE"
    },
    "DateCreated": {
        "mysqltype": "date",
        "sqlalchemytype": Date,
        "alias": "DATE_CREATED"
    },
    "primary_key": "BookID"
}

# Pages of book are single documents.
# Links and information to pages recorded in table
columns_booktable = {
    "DocumentName": {
        "mysqltype": "text",
        "sqlalchemytype": Text,
        "alias": "DOCUMENT_NAME"
    },
    "DocumentType": {
        "mysqltype": "text",
        "sqlalchemytype": Text,
        "alias": "DOCUMENT_TYPE"
    },
    "Path": {
        "mysqltype": "text",
        "sqlalchemytype": Text,
        "alias": "PATH"
    },
    "BookID": {
        "mysqltype": "text",
        "sqlalchemytype": Text,
        "alias": "BOOK_ID"
    },
    "primary_key": "PageID"
}

def find_optional_columns(table, table_type, aliasnames=True):
    cols_standard = column_types_table(
        table_type,
        optional_columns=[],
        remove_primarykey=True,
        return_aliasnames=aliasnames
    )
    if aliasnames:
        return list(set(table.columns) - set(cols_standard))
    else:
        return list(
            set(table.columns) - set([key for (key, value) in cols_standard.items()])
        )

def column_types_table(
        table_type,
        optional_columns=[],
        remove_primarykey=False,
        return_aliasnames=False
):
    if table_type == "browsing":
        dct = columns_browsingtable.copy()
    elif table_type == "book":
        dct = columns_booktable.copy()
    elif table_type == "books":
        dct = columns_bookstable.copy()
    elif table_type == "photo":
        dct = columns_phototable.copy()
    elif table_type == "photos":
        dct = columns_photostable.copy()
    elif table_type == "events":
        dct = columns_eventsstable.copy()
    else:
        raise ValueError("Table type unknown")

    # Add default columns
    dct.update(columns_common)

    # Optional columns
    # Can be either alias of key
    if len(optional_columns) != 0:
        dct_optional = columns_optional.copy()
        # TODO Not nice
        dct.update(
            {key: value for (key, value) in dct_optional.items() if (
                    (value["alias"] in optional_columns) or (key in optional_columns)
            )}
        )

    if remove_primarykey:
        dct.pop("primary_key")

    if return_aliasnames:
        # Return list
        dct = [value["alias"] for (key, value) in dct.items()]

    return dct

