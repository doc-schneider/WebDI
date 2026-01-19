import os
import io
from pathlib import Path
import pandas as pd
from datetime import datetime, timedelta
from azure.storage.blob import ContainerClient, BlobServiceClient, generate_blob_sas, BlobSasPermissions
from azure.core.exceptions import ResourceExistsError
from azure.identity import DefaultAzureCredential, AzureCliCredential
from azure.keyvault.secrets import SecretClient


class AzureFactory:
    @staticmethod
    def get_storage_key(environment):
        if environment == 'LOCAL':
            key = os.getenv("AZURE_STORAGE_KEY")
        else:
            # credential = DefaultAzureCredential()
            credential = AzureCliCredential()  # Only for local testing
            secret_client = SecretClient(vault_url="https://docschneider-keyvault.vault.azure.net/", credential=credential)
            secret = secret_client.get_secret("keyStorage")
            key = secret.value
        return key

    @staticmethod
    def connection_string(environment):
        key = AzureFactory.get_storage_key(environment)
        return 'DefaultEndpointsProtocol=https;AccountName=docschneiderstorage;AccountKey=' + key + \
               ';EndpointSuffix=core.windows.net'

    @staticmethod
    def create_blob_service_client(connection_string):
        return BlobServiceClient.from_connection_string(connection_string)

    @staticmethod
    def create_container(container_name, environment):
        # Create container if not existing
        blob_service_client = BlobServiceClient.from_connection_string(AzureFactory.connection_string(environment))
        try:
            new_container = blob_service_client.create_container(container_name)
        except ResourceExistsError:
            print("Container already exists.")

    @staticmethod
    def create_blob_sas(container_name, blob_name, environment):
        key = AzureFactory.get_storage_key(environment)
        sas = generate_blob_sas(
                account_name="docschneiderstorage",
                container_name=container_name,
                blob_name=blob_name,
                account_key=key,
                permission=BlobSasPermissions(read=True),
                expiry=datetime.utcnow() + timedelta(hours=3),
        )
        return sas

    @staticmethod
    def upload_from_table_to_blob(container_name, path_blob, table):
        # Uploads content of local directory to analogous blob-container structure based on information in Data table.
        PATH_AZURE_BLOB = list()
        for i in range(len(table.table)):
            file_name = table.table.loc[i, 'FILE_NAME']
            path_name = AzureFactory.convert_path_to_blob(table.table['PATH'].iloc[i])
            blob_name = path_name.replace(path_blob, '') + "/" + file_name
            # blob_name = path_blob + "/" + file_name
            with open(Path(path_name, file_name), "rb") as data:
                AzureFactory.upload_blob(container_name, blob_name, data)
            # Add Azure path to table
            PATH_AZURE_BLOB.append(blob_name)
        return PATH_AZURE_BLOB

    @staticmethod
    def upload_blob(container_name, blob_name, data, flag_overwrite=True):
        blob_service_client = AzureFactory.create_blob_service_client(
            AzureFactory.connection_string("LOCAL")
        )
        blob_client = blob_service_client.get_blob_client(container_name, blob_name)
        blob_client.upload_blob(
            data,
            overwrite=flag_overwrite,
            max_concurrency=1,           # stabiler bei schlechten Netzen
            blob_type="BlockBlob",
            timeout=300                  # Sekunden
        )

    @staticmethod
    def download_blob(container_name, blob_name, environment, stream=None):
        container_client = ContainerClient.from_connection_string(
            conn_str=AzureFactory.connection_string(environment),
            container_name=container_name
        )
        if not stream:
            return container_client.download_blob(blob_name).readall()
        else:
            container_client.download_blob(blob_name).readinto(stream)
            return stream   # TODO return not necessary (?)

    @staticmethod
    def read_table_from_blob(container_name, blob_name, environment):
        return pd.read_csv(
            io.BytesIO(
                AzureFactory.download_blob(
                    container_name, blob_name, environment
                )
            ), sep=";"
        )  # TODO StringIO? sep shouldnt be necessary?

    # @staticmethod
    # def read_csv_from_blob(container_name, blob_name, environment):
    #     csv_data = AzureFactory.download_blob(
    #         container_name, blob_name, environment
    #     ).decode("utf-8")
    #     return pd.read_csv(
    #         io.StringIO(csv_data)
    #     )

    @staticmethod
    def write_table_to_blob(container_name, blob_name, table):
        csv_buffer = table.write_table_to_csv()
        AzureFactory.upload_blob(container_name, blob_name, csv_buffer.getvalue())

    @staticmethod
    def convert_path_to_blob(path_str):
        return path_str.replace("\\", "/")
