# 🔒 Self-Destructing File Share

A secure, lightweight web application built with Python and Streamlit that allows users to upload files and generate time-limited, read-only download links using Azure Blob Storage. 

This project demonstrates core cloud storage concepts including container management, metadata tagging, Shared Access Signatures (SAS), and programmatic resource lifecycle management.

## ✨ Features

* **Secure File Uploads:** Upload files directly to a private Azure Blob Storage container.
* **Time-Limited Access:** Generate secure, read-only Shared Access Signature (SAS) URLs valid for a user-defined duration (e.g., 5 minutes to 24 hours).
* **Metadata Tagging:** Files are automatically tagged with a strict UTC expiry timestamp upon upload.
* **Automatic Collision Prevention:** File uploads are prefixed with a UUID to prevent overwriting existing blobs with the same name.
* **Admin Purge Tool:** A built-in administrative sidebar that scans container metadata and physically deletes files whose access links have expired, optimizing cloud storage costs.

## 🛠️ Technology Stack

* **Frontend/Backend:** [Streamlit](https://streamlit.io/) (Python)
* **Cloud Provider:** Microsoft Azure
* **Storage:** Azure Blob Storage
* **SDK:** `azure-storage-blob`

## 🚀 Local Development Setup

### 1. Prerequisites
* Python 3.8 or newer installed.
* An active Azure Storage Account.
* Your Azure Storage Account Connection String.

### 2. Clone the Repository
```bash
git clone [https://github.com/yourusername/self-destructing-azure-share.git](https://github.com/yourusername/self-destructing-azure-share.git)
cd self-destructing-azure-share
```

### 3. Set Up a Virtual Environment
Create and activate an isolated Python environment:
```powershell
# Windows / PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies
Install the required packages using pip:
```bash
pip install streamlit azure-storage-blob
```

### 5. Configure Environment Variables
To securely connect to Azure, set your connection string as an environment variable. **Never hardcode your connection string into the application files.**

```powershell
# Windows (permanently saves to your user profile, requires terminal restart)
setx AZURE_STORAGE_CONNECTION_STRING "your_connection_string_here"

# macOS / Linux (temporary for the current session)
export AZURE_STORAGE_CONNECTION_STRING="your_connection_string_here"
```

### 6. Run the Application
Launch the Streamlit server:
```bash
streamlit run app.py
```
The application will automatically open in your default web browser at `http://localhost:8501`. On the first run, the app will automatically create a private container named `shares` in your Azure Storage Account if it does not already exist.

## 🔒 Security Best Practices

* **.gitignore:** Ensure your `.venv/` folder and any `.env` files are included in your `.gitignore` to prevent leaking credentials or uploading unnecessary environment files.
* **SAS Tokens:** The application generates standard read-only SAS tokens. If a token expires, Azure will return a `403 Forbidden` error, blocking access to the file while it awaits physical deletion via the Admin Purge tool.
