from dotenv import load_dotenv

from Initialize.Initialize import initialize_MySQL
from DataStructures.Data import DataTable
from DataStructures.TableTypes import TableType
from DataOperations.Azure import AzureFactory
from DataOperations.MySQL import update_column
import config

load_dotenv()
config.environment_storage = "AZURE"
config.environment_app = "LOCAL"
initialize_MySQL()

# Get meta table from Database
album_table = DataTable.fetch_table(
    TableType.ALBUM,
    "albums"
)
album_table = album_table.filter({"ID_ALBUM": 7})
# Upload to blob
#csv_buffer = album_table.write_table_to_csv()
#AzureFactory.upload_blob("tables", "albums.csv", csv_buffer.getvalue())
# Get file table and upload
photo_table = DataTable.fetch_table(
    TableType.PHOTO,
    "photos"
).filter({"ID_ALBUM": 7})
csv_buffer = photo_table.write_table_to_csv()
AzureFactory.upload_blob("tables", "photos.csv", csv_buffer.getvalue())
# Upload files to blob
PATH_AZURE_BLOB = AzureFactory.upload_from_table_to_blob("photo", "Y:/", photo_table)
# Write blob  names to table
value_dct = dict(zip(photo_table.table["ID_PHOTO"], PATH_AZURE_BLOB))
update_column(
    config.mysql["connector"], config.mysql["cursor"],
    "photos", "AZURE_BLOB", "ID_PHOTO", value_dct
)

print("done")
