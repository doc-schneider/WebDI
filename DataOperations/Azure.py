from azure.storage.blob import BlobClient, ContainerClient, BlobServiceClient
from azure.core.exceptions import ResourceExistsError
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

from DataOperations.Utilities import add_thumbnail_to_filename


class AzureFactory:

    @staticmethod
    def connection_string():
        credential = DefaultAzureCredential()
        secret_client = SecretClient(vault_url="https://docschneider-keyvault.vault.azure.net/", credential=credential)
        secret = secret_client.get_secret("keyStorage")
        return 'DefaultEndpointsProtocol=https;AccountName=docschneiderstorage;AccountKey=' + secret.value + \
               ';EndpointSuffix=core.windows.net'

    @staticmethod
    def create_container(container_name):
        # Create container if not existing
        blob_service_client = BlobServiceClient.from_connection_string(AzureFactory.connection_string())
        try:
            new_container = blob_service_client.create_container(container_name)
        except ResourceExistsError:
            print("Container already exists.")

    @staticmethod
    def upload_blob(container_name, path_container, table, use_thumbnail=False):
        # Uploads content of local directory to analogous blob-container structure.
        # Based on information in document table.
        # Mode for uploading of thumbnails

        # Create container if not existing
        AzureFactory.create_container(container_name)

        PATH_AZURE_CONTAINER = list()
        PATH_AZURE_BLOB = list()
        for i in range(table.length):
            print(i)
            file_name = table.data['DOCUMENT_NAME'].iloc[i]
            path_name = table.data['PATH'].iloc[i]
            if use_thumbnail:
                file_name = \
                    add_thumbnail_to_filename(file_name, table.data['DOCUMENT_TYPE'].iloc[i][0])
            blob_name = path_name.replace(path_container, '') + file_name
            blob = BlobClient.from_connection_string(conn_str=AzureFactory.connection_string(),
                                                 container_name=container_name,
                                                 blob_name=blob_name)
            with open(path_name + file_name, "rb") as data:
                blob.upload_blob(data, overwrite=True, connection_timeout=120) # TODO: Understand timeout
            # Add Azure path to table
            PATH_AZURE_CONTAINER.append(container_name)
            PATH_AZURE_BLOB.append(blob_name)
        return PATH_AZURE_CONTAINER, PATH_AZURE_BLOB

    @staticmethod
    def download_blob_single(container_name, blob_name):
        container_client = ContainerClient.from_connection_string(
            conn_str=AzureFactory.connection_string(),
            container_name=container_name
        )
        return container_client.download_blob(blob_name)
