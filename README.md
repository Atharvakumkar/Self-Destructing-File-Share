# Self-Destructing File Share

A lightweight, cloud-based file-sharing application built with Python, Streamlit, and Microsoft Azure Blob Storage. The application generates time-limited, read-only download links for uploaded files and provides an administrative tool for deleting expired files.

The project demonstrates practical cloud engineering concepts, including object storage, Shared Access Signatures (SAS), metadata management, access expiry, and automated resource cleanup.

## Key Features

- **Secure File Uploads:** Upload files to a private Azure Blob Storage container.
- **Time-Limited File Sharing:** Generate read-only SAS URLs with configurable expiry durations ranging from 5 minutes to 24 hours.
- **Metadata-Based Expiry:** Attach UTC expiry timestamps to uploaded blobs to support lifecycle management.
- **Unique Blob Naming:** Prefix uploaded filenames with UUIDs to reduce naming collisions and prevent accidental overwrites.
- **Administrative Cleanup:** Scan blob metadata and permanently delete files whose configured expiry times have passed.
- **Cloud-Based Storage:** Store uploaded files in Azure Blob Storage rather than relying exclusively on local application storage.

## Technology Stack

| Category | Technology |
|---|---|
| Programming Language | Python |
| Application Framework | Streamlit |
| Cloud Provider | Microsoft Azure |
| Object Storage | Azure Blob Storage |
| Azure SDK | `azure-storage-blob` |
| File Identification | UUID |
| Time Management | UTC timestamps |
| Access Control | Shared Access Signatures (SAS) |

## Architecture Overview

The application uses Azure Blob Storage to store files and control access through time-limited SAS URLs.

```text
                 ┌────────────────────────┐
                 │        User            │
                 └────────────┬───────────┘
                              │
                              ▼
                 ┌────────────────────────┐
                 │   Streamlit Interface  │
                 └────────────┬───────────┘
                              │
                  ┌───────────┴───────────┐
                  │                       │
                  ▼                       ▼
       ┌──────────────────┐   ┌────────────────────┐
       │  File Upload     │   │ SAS URL Generation │
       │  and Metadata    │   │ with Expiry        │
       └────────┬─────────┘   └──────────┬─────────┘
                │                        │
                ▼                        ▼
       ┌──────────────────┐   ┌────────────────────┐
       │ Azure Blob       │   │ Time-Limited       │
       │ Storage          │   │ Read-Only Access   │
       └────────┬─────────┘   └────────────────────┘
                │
                ▼
       ┌──────────────────┐
       │ Admin Purge Tool │
       │ Expired Blob     │
       │ Deletion         │
       └──────────────────┘
```

### Workflow

1. A user uploads a file through the Streamlit interface.
2. The application assigns a UUID-prefixed blob name to reduce filename collisions.
3. The file is uploaded to a private Azure Blob Storage container.
4. The application records an expiry timestamp in the blob metadata.
5. A read-only SAS URL is generated with a configured expiration time.
6. The recipient can access the file through the URL until the SAS token expires, subject to Azure Storage authorization and account configuration.
7. An administrator can run the purge tool to identify and permanently delete expired blobs.

> **Important:** SAS expiry and physical file deletion are separate operations. A file can remain in storage after its download link expires until the cleanup process deletes it.

## Getting Started

### Prerequisites

Ensure the following are available:

- Python 3.8 or newer, subject to compatibility with the installed dependencies.
- An Azure subscription.
- An Azure Storage Account.
- An Azure Storage Account connection string.
- Git.

### 1. Clone the Repository

Replace the placeholder repository URL with the actual URL of your GitHub repository.

```bash
git clone <YOUR_REPOSITORY_URL>
cd <YOUR_REPOSITORY_DIRECTORY>
```

### 2. Create a Virtual Environment

**Windows — PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install streamlit azure-storage-blob
```

If the repository contains a `requirements.txt` file, install the project's pinned dependencies instead:

```bash
python -m pip install -r requirements.txt
```

### 4. Configure Azure Credentials

Set the `AZURE_STORAGE_CONNECTION_STRING` environment variable.

**Windows — PowerShell**

```powershell
$env:AZURE_STORAGE_CONNECTION_STRING = "your_connection_string_here"
```

This setting applies to the current PowerShell session.

To persist the variable for future sessions, you can use:

```powershell
setx AZURE_STORAGE_CONNECTION_STRING "your_connection_string_here"
```

Restart the terminal after using `setx`.

**macOS / Linux**

```bash
export AZURE_STORAGE_CONNECTION_STRING="your_connection_string_here"
```

Obtain the connection string from your Azure Storage Account settings.

**Security warning:** A storage account connection string may grant substantial access to storage resources. Never commit it to GitHub or expose it in screenshots, logs, or application output.

### 5. Run the Application

```bash
streamlit run app.py
```

Open the local address displayed in the terminal. The default Streamlit address is:

```text
http://localhost:8501
```

According to the current project documentation, the application creates a private container named `shares` if it does not already exist.

### 6. Test File Sharing

1. Upload a test file.
2. Select an expiry duration.
3. Generate the sharing URL.
4. Open the URL to verify that the file can be downloaded.
5. Wait until the SAS token expires and test access again.
6. Use the administrative purge tool to verify that expired files are removed.

Use non-sensitive test files when validating the application.

## Security Considerations

### 1. Protect Azure Credentials

- Store connection strings in environment variables or a suitable secrets manager.
- Add `.venv/`, `.env`, and other local configuration files to `.gitignore`.
- Never commit storage account keys or privileged credentials.
- Rotate credentials immediately if they are accidentally exposed.

### 2. Apply Least-Privilege Access

Use the narrowest practical Azure permissions for each operation. Where supported by the implementation, consider Microsoft Entra ID authentication and managed identities instead of long-lived storage account keys.

### 3. Restrict SAS Permissions

SAS URLs should grant only the permissions required by the recipient.

For read-only downloads:

- Grant read access only.
- Use the shortest practical expiry duration.
- Avoid granting upload, write, or delete permissions.
- Consider HTTPS-only access and appropriate SAS signing mechanisms.

Anyone who obtains a valid SAS URL may be able to use it until it expires or is otherwise invalidated.

### 4. Protect Administrative Operations

The purge tool permanently deletes files. Restrict access to this functionality and ensure that administrative actions cannot be triggered by unauthorized users.

### 5. Validate Expiry and Deletion Behavior

- Use UTC consistently when storing and comparing expiry timestamps.
- Handle missing or malformed metadata safely.
- Account for timezone and clock differences.
- Test cleanup behavior before deploying the application with real user files.

> **Implementation note:** The actual security guarantees depend on the SAS-generation logic, Azure Storage configuration, authentication controls, and administrative authorization implemented in the application.

## Limitations

- Files may remain in Azure Blob Storage after their SAS URLs expire until the purge process runs.
- A SAS URL can be shared with other people while it remains valid.
- The application requires appropriate Azure Storage configuration and credentials.
- The effectiveness of administrative cleanup depends on the purge process running successfully.
- Expired-link behavior does not, by itself, guarantee immediate or permanent deletion of all copies of a file.

