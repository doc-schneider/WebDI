from azure.storage.blob import BlobClient

from DataStructures.Data import DataTableFactory, DataTable
from DataOperations.Azure import AzureFactory


path_root = '//192.168.178.53/'

# Load table
table_name = 'Startliste_Papa_utf8'
path_table = path_root + 'Stefan/DigitalImmortality/Document and Event Tables/' + table_name + '.csv'
table = DataTable(DataTableFactory.importFromCsv(path_table))

## Write table from csv
table_name_azure = table_name
blob = BlobClient.from_connection_string(conn_str=AzureFactory.connection_string(),
                                         container_name='modest-di',
                                         blob_name='tables/'+table_name_azure)
with open(path_table, "rb") as data:
    blob.upload_blob(data, overwrite=True)

## Upload blobs
#path_container = 'Fotos/'  # 'Musik/'
#container_name = 'photo'  # 'music'
#PATH_AZURE_CONTAINER, PATH_AZURE_BLOB = \
#    AzureFactory.upload_blob(container_name, path_root + path_container, table)
#table.data['PATH_AZURE_CONTAINER'] = PATH_AZURE_CONTAINER
#table.data['PATH_AZURE_BLOB'] = PATH_AZURE_BLOB
# Upload thumbnails
#AzureFactory.upload_blob(container_name, path_root + path_container, table, True)

# Upload table
# TODO Write table to csv back (with Azure information)