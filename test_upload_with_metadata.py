import os
import datetime
from azure.storage.blob import BlobServiceClient

conn_str = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
blob_service_client = BlobServiceClient.from_connection_string(conn_str)

container_name = "shares"
blob_name = "test-sample.txt"
file_content = "Hello from Azure Blob Storage! This is a test file."

# Calculate an expiry timestamp 1 hour from now (in UTC, ISO format)
expiry_time = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)).isoformat()

# Metadata keys in Azure must be valid ASCII identifiers
metadata = {
    "expiry": expiry_time,
    "original_filename": "sample.txt"
}

print(f"Uploading '{blob_name}' to container '{container_name}'...")

# Get a BlobClient targeting the specific file path inside the container
blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

# Upload data (overwrite=True ensures we can run the test script multiple times safely)
blob_client.upload_blob(
    data=file_content,
    overwrite=True,
    metadata=metadata
)

print(f"File uploaded successfully with expiry metadata: {expiry_time}")