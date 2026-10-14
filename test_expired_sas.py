import os
import datetime
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions

conn_str = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
blob_service_client = BlobServiceClient.from_connection_string(conn_str)

container_name = "shares"
blob_name = "test-sample.txt"

account_name = blob_service_client.account_name
account_key = blob_service_client.credential.account_key

now = datetime.datetime.now(datetime.timezone.utc)
# Start 1 minute in the past for clock tolerance
start_time = now - datetime.timedelta(minutes=1)
# Expire strictly 45 seconds from now
expiry_time = now + datetime.timedelta(seconds=45)

sas_token = generate_blob_sas(
    account_name=account_name,
    container_name=container_name,
    blob_name=blob_name,
    account_key=account_key,
    permission=BlobSasPermissions(read=True),
    start=start_time,
    expiry=expiry_time
)

blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
full_url = f"{blob_client.url}?{sas_token}"

print("Link valid for ~45 seconds:")
print(full_url)