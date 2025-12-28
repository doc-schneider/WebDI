import pandas as pd
from dotenv import load_dotenv

from Initialize.Initialize import initialize_MySQL
from DataStructures.Data import DataTable
from DataStructures.TableTypes import TableType
from DataOperations.Azure import AzureFactory
from DataOperations.MySQL import update_column
import config

load_dotenv()
config.environment_app = "LOCAL"
initialize_MySQL()

# New Container
#
# container_name = "film"
# AzureFactory.create_container(container_name, config.environment_app)


# Upload films
#
config.environment_storage = "LOCAL"
film_table_mysql = DataTable.fetch_table(
    TableType.FILM,
    "films"
)
film_content_table_mysql = DataTable.fetch_table(
    TableType.FILM_CONTENT,
    "film_contents"
)
# TODO Filter
#
# Upload films files
PATH_AZURE_BLOB = AzureFactory.upload_from_table_to_blob("film", "Papa_VHS", film_table_mysql)
# Add Blob information
film_table_mysql.table["AZURE_BLOB"] = PATH_AZURE_BLOB
film_table_mysql.table["AZURE_CONTAINER"] = "film"
#
# Upload tables to blob
AzureFactory.write_table_to_blob("tables", "films.csv", film_table_mysql)
AzureFactory.write_table_to_blob("tables", "film_contents.csv", film_content_table_mysql)
#
# Write blob  names to MySQL table
value_dct = dict(zip(film_table_mysql.table["ID_FILM"], PATH_AZURE_BLOB))
update_column(
    config.mysql["connector"], config.mysql["cursor"],
    "films", "AZURE_BLOB", "ID_FILM", value_dct
)
value_dct = dict(zip(film_table_mysql.table["ID_FILM"], ["film"] * film_table_mysql.table.shape[0]))
update_column(
    config.mysql["connector"], config.mysql["cursor"],
    "films", "AZURE_CONTAINER", "ID_FILM", value_dct
)


# Upload Message Collection
#
ID_MESSAGE_COLLECTION = 1
#
# Get message table and upload
#
config.environment_storage = "LOCAL"
message_table_mysql = DataTable.fetch_table(
    TableType.MESSAGE,
    "messages"
).filter({"ID_MESSAGE_COLLECTION": ID_MESSAGE_COLLECTION})


# Upload photo album
#
ID_ALBUM = 195
#
# Get meta table from Database
config.environment_storage = "LOCAL"
album_table_mysql = DataTable.fetch_table(
    TableType.ALBUM,
    "albums"
)
album_table_mysql = album_table_mysql.filter({"ID_ALBUM": ID_ALBUM})
# From Azure
config.environment_storage = "AZURE"
album_table_azure = DataTable.fetch_table(
    TableType.ALBUM,
    "albums.csv"
)
# Append
album_table = DataTable(
    pd.concat([album_table_mysql.table, album_table_azure.table], ignore_index=True),
    TableType.ALBUM,
)
# Upload to blob
AzureFactory.write_table_to_blob("tables", "albums.csv", album_table)
#
# Get file table and upload
#
config.environment_storage = "LOCAL"
photo_table_mysql = DataTable.fetch_table(
    TableType.PHOTO,
    "photos"
).filter({"ID_ALBUM": ID_ALBUM})
# Add container name
photo_table_mysql.table["AZURE_CONTAINER"] = "photo"
# From Azure
config.environment_storage = "AZURE"
photo_table_azure = DataTable.fetch_table(
    TableType.PHOTO,
    "photos.csv"
)
# Upload files to blob
PATH_AZURE_BLOB = AzureFactory.upload_from_table_to_blob("photo", "Y:/", photo_table_mysql)
# Add Blob information
photo_table_mysql.table["AZURE_BLOB"] = PATH_AZURE_BLOB
# Append
photo_table = DataTable(
    pd.concat([photo_table_azure.table, photo_table_mysql.table], ignore_index=True),
    TableType.PHOTO,
)
# Upload table to blob
AzureFactory.write_table_to_blob("tables", "photos.csv", photo_table)
# Write blob  names to MySQL table
value_dct = dict(zip(photo_table_mysql.table["ID_PHOTO"], PATH_AZURE_BLOB))
update_column(
    config.mysql["connector"], config.mysql["cursor"],
    "photos", "AZURE_BLOB", "ID_PHOTO", value_dct
)
value_dct = dict(zip(photo_table_mysql.table["ID_PHOTO"], ["photo"] * photo_table_mysql.table.shape[0]))
update_column(
    config.mysql["connector"], config.mysql["cursor"],
    "photos", "AZURE_CONTAINER", "ID_PHOTO", value_dct
)

print("done")
