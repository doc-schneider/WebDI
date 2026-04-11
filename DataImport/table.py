import pandas as pd

from Initialize.Initialize import initialize_MySQL
from DataStructures.TableTypes import TableType, table_definitions, table_columns_names_types
from DataStructures.Data import DataTable
from DataOperations.MySQL import create_table, create_table_mysql, table_insert, add_columns, add_foreign_key, update_column, delete_record
import config

config.environment_storage = "LOCAL"
initialize_MySQL()

# Remove photo records wiht wrong ID_ALBUM
#
album_table = DataTable.fetch_table(TableType.ALBUM, "albums")
photo_table = DataTable.fetch_table(TableType.PHOTO, "photos")
# All albums with mulitply used name
album_names = album_table.table["PHOTO_ALBUM"].unique()
for a_n in album_names:
    a_id = album_table.table.loc[album_table.table["PHOTO_ALBUM"] == a_n, "ID_ALBUM"].values
    if a_id.size > 1:
        # All photos belonging to this album name
        photos = photo_table.table.loc[
            photo_table.table["PHOTO_ALBUM"] == a_n,
            ["FILE_NAME", "DATE_TIME", "ID_ALBUM", "ID_PHOTO"]
        ]
        # Names possibly not unique
        photos_unique = photos[["FILE_NAME", "DATE_TIME"]].drop_duplicates()
        for index, row in photos_unique.iterrows():
            df = photos.loc[
                (photos["FILE_NAME"] == row["FILE_NAME"]) & (photos["DATE_TIME"] == row["DATE_TIME"]),
                :
            ]
            if df.shape[0] > 1:
                # Last entry is the right one
                for id in df.sort_values("ID_ALBUM")["ID_PHOTO"].values[:-1]:
                    delete_record(
                        config.mysql["connector"], config.mysql["cursor"],
                        "photos", "ID_PHOTO", int(id)
                    )
# Delete Table
#

# Create table
#
# create_table(db_engine, metadata, "documents", table_definitions[TableType.DOCUMENT], foreign_table="document_collections")
create_table_mysql(
    config.mysql["connector"], config.mysql["cursor"],
    "photo_pages",
    table_definitions[TableType.PHOTO_PAGE],
    foreign_table_name="albums",
    foreign_table_dct=table_definitions[TableType.ALBUM],
)

# Add foreign key column
#
foreign_table = "events"
foreign_column = table_definitions[TableType.EVENT]["PrimaryKey"]
add_foreign_key(conn, mycursor, "photos", foreign_column, foreign_table)

# Add column
table_name = "document_collections"
add_columns(
    config.mysql["connector"], config.mysql["cursor"],
    table_name, {
        "OWNER": table_columns_names_types["OWNER"]["mysqltype"],
    }
)

# Delete column
table_name = "albums"
column_name = "TAG"
query = f'ALTER TABLE {table_name} DROP COLUMN {column_name};'
mycursor.execute(query)
conn.commit()

# Set column values
table_name = "albums"
column_set = "CONTENT_TYPE"
# update_column()
query = f"UPDATE {table_name} SET {column_set} =  %s"
# column_if = "ID_EVENT"
# query = f"UPDATE {table_name} SET {column_set} =  CASE WHEN {column_if} = 24 THEN 5 END;"
config.mysql["cursor"].execute(query, ("PHOTO", ))
config.mysql["connector"].commit()

# Fetch table subset (where)
#
table_name = "albums"
column_name = "ID_ALBUM"
value = 6
query = f"SELECT * FROM {table_name} WHERE {column_name} = {value}"
tbl = pd.read_sql(query, con=conn)









