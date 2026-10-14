import os
import streamlit as st
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError
import uuid
import datetime
from azure.storage.blob import generate_blob_sas, BlobSasPermissions
import zoneinfo

# 1. Page setup
st.set_page_config(page_title="Self-Destructing File Share")
st.title("Self-Destructing File Share")

# 2. Connect to Azure securely
conn_str = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
if not conn_str:
    st.error("Missing AZURE_STORAGE_CONNECTION_STRING environment variable. Did you run setx and restart the terminal?")
    st.stop() # Halts the app so it doesn't crash on the next line

blob_service_client = BlobServiceClient.from_connection_string(conn_str)
container_name = "shares"

# 3. Ensure the target container exists
try:
    blob_service_client.create_container(container_name)
except ResourceExistsError:
    pass # Container already exists, which is exactly what we want

# 4. UI Elements for file upload and expiry selection
st.subheader("Upload a File")
uploaded_file = st.file_uploader("Choose a file to securely share")

# Dictionary mapping human-readable options to minutes
expiry_options = {
    "1 minute": 1,
    "5 minutes": 5,
    "10 minutes": 10,
    "1 hour": 60,
    "24 hours": 1440
}

# Create a dropdown menu using the dictionary keys
selected_expiry = st.selectbox("How long should the link be valid?", options=list(expiry_options.keys()))

# 5. Core logic to upload and generate the link
def upload_and_share(file, expiry_minutes):
    # Create a unique filename to prevent overwriting
    unique_name = f"{uuid.uuid4()}-{file.name}"
    
    # Calculate strict expiry timestamp for the metadata (in UTC)
    now = datetime.datetime.now(datetime.timezone.utc)
    expiry_time = now + datetime.timedelta(minutes=expiry_minutes)
    metadata = {"expiry": expiry_time.isoformat()}
    
    # Upload the file with metadata
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=unique_name)
    blob_client.upload_blob(file, overwrite=True, metadata=metadata)
    
    # Generate the SAS token (start 5 mins in the past for clock skew)
    sas_token = generate_blob_sas(
        account_name=blob_service_client.account_name,
        container_name=container_name,
        blob_name=unique_name,
        account_key=blob_service_client.credential.account_key,
        permission=BlobSasPermissions(read=True),
        start=now - datetime.timedelta(minutes=5),
        expiry=expiry_time
    )
    
    # Construct and return the full URL
    return f"{blob_client.url}?{sas_token}", expiry_time

# 7. Purge Expired Blobs function
def purge_expired_blobs():
    container_client = blob_service_client.get_container_client(container_name)
    
    # List blobs and include their metadata in a single API call
    blob_list = container_client.list_blobs(include=['metadata'])
    
    now = datetime.datetime.now(datetime.timezone.utc)
    deleted_count = 0
    
    for blob in blob_list:
        # Check if the blob has our custom 'expiry' metadata
        if blob.metadata and 'expiry' in blob.metadata:
            try:
                # Convert the ISO string back into a Python datetime object
                expiry_time = datetime.datetime.fromisoformat(blob.metadata['expiry'])
                
                # If the current time is strictly greater than the expiry time, delete it
                if now > expiry_time:
                    container_client.delete_blob(blob.name)
                    deleted_count += 1
            except ValueError:
                pass # Skip if the date string is somehow malformed
                
    return deleted_count

# 8. Sidebar UI for the Admin controls
with st.sidebar:
    st.header("Admin Controls")
    st.write("Click below to physically delete any files whose links have expired.")
    if st.button("🧹 Purge Expired Files"):
        with st.spinner("Scanning for expired files..."):
            count = purge_expired_blobs()
            if count > 0:
                st.success(f"Deleted {count} expired file(s)!")
            else:
                st.info("No expired files found.")

# 6. Button to trigger the process
if uploaded_file is not None:
    if st.button("Generate Secure Link"):
        with st.spinner("Uploading to Azure..."):
            # Get the actual integer minutes from our dictionary
            minutes = expiry_options[selected_expiry]
            
            # Call our function
            link, expiry_timestamp = upload_and_share(uploaded_file, minutes)
            
            # Display results
            st.success("File uploaded successfully!")
            st.markdown(f"**Your secure link:** [Click here to download]({link})")
            
            # Show a friendly formatted time
            # Convert the UTC time to IST for the UI display
            ist_time = expiry_timestamp.astimezone(zoneinfo.ZoneInfo("Asia/Kolkata"))
            st.info(f"Link expires at: {ist_time.strftime('%Y-%m-%d %I:%M:%S %p IST')}")