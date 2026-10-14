import os
from azure.storage.blob import BlobServiceClient

# 1. Read the connection string from the environment variable
# If this is None, it means the variable wasn't set correctly or the terminal wasn't restarted
conn_str = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')

if not conn_str:
    print("ERROR: Could not find AZURE_STORAGE_CONNECTION_STRING environment variable.")
    exit(1)

# 2. Create the BlobServiceClient
print("Connecting to Azure...")
blob_service_client = BlobServiceClient.from_connection_string(conn_str)

# 3. List all containers (like S3 buckets) in this storage account
print("Connected! Listing containers:")
containers = blob_service_client.list_containers()

count = 0
for container in containers:
    print(f" - {container['name']}")
    count += 1

if count == 0:
    print(" (No containers found. The storage account is empty.)")