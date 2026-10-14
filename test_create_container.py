import os
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError

conn_str = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
blob_service_client = BlobServiceClient.from_connection_string(conn_str)

container_name = "shares"

print(f"Creating container '{container_name}'...")

try:
    # create_container makes the container with private access by default
    container_client = blob_service_client.create_container(container_name)
    print(f"Container '{container_name}' created successfully!")
except ResourceExistsError:
    print(f"Container '{container_name}' already exists.")