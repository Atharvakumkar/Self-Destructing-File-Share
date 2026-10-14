import os
import datetime
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions

# 1. Connect to Azure
conn_str = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
blob_service_client = BlobServiceClient.from_connection_string(conn_str)

container_name = "shares"
blob_name = "test-sample.txt"

# 2. Extract the account name and root access key from our client
account_name = blob_service_client.account_name
account_key = blob_service_client.credential.account_key

# 3. Define the time window for the SAS token
# We start it 5 minutes in the past to prevent "clock skew" errors,
# where Azure's servers think the token isn't valid yet because of minor clock differences.
now = datetime.datetime.now(datetime.timezone.utc)
start_time = now - datetime.timedelta(minutes=5)
expiry_time = now + datetime.timedelta(hours=1)

# 4. Generate the cryptographic token string granting read permissions
sas_token = generate_blob_sas(
    account_name=account_name,
    container_name=container_name,
    blob_name=blob_name,
    account_key=account_key,
    permission=BlobSasPermissions(read=True),
    start=start_time,
    expiry=expiry_time
)

# 5. Construct the full URL by appending the token to the base blob URL
blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
full_url = f"{blob_client.url}?{sas_token}"

print("Your temporary download link is:")
print(full_url)