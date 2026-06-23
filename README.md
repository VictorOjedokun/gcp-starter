# GCP Cloud Storage Starter — Python

A Python starter for interacting with Google Cloud Storage (GCS). Upload, download, list, delete objects, and generate signed URLs. Built and tested on a GCP VM.

---

## Project structure

```
gcp-storage-starter/
├── src/
│   ├── storage.py      # GCS helper functions
│   └── example.py      # Runnable demo
├── tests/
│   └── test_storage.py # Unit tests (mocked — no real credentials needed)
├── .github/
│   └── workflows/
│       └── ci.yml      # GitHub Actions: lint + test on push/PR
├── requirements.txt
└── .gitignore
```

---

## Setup on a GCP VM

### 1. Install dependencies

SSH into your VM from the GCP Console (**Compute Engine → VM Instances → SSH**), then run:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git python3 python3-pip python3-venv
```

### 2. Clone and install

```bash
git clone https://github.com/<your-username>/gcp-storage-starter.git
cd gcp-storage-starter
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

> You'll need to run `source .venv/bin/activate` every time you open a new terminal session.

### 3. Create a GCS bucket

1. Go to **GCP Console → Cloud Storage → Buckets → Create bucket**
2. Give it a globally unique name and choose a region close to your VM
3. Set the bucket name on your VM:

```bash
export BUCKET_NAME="your-bucket-name"

# To make it permanent across reboots:
echo 'export BUCKET_NAME="your-bucket-name"' >> ~/.bashrc
source ~/.bashrc
```

### 4. Fix VM API scopes

By default, GCP VMs are created with restricted API scopes which block access to Cloud Storage and other services. You'll see this error if scopes aren't updated:

```
403 Provided scope(s) are not authorized
```

Fix it from **Cloud Shell** (click the `>_` icon in the GCP Console — do NOT run this from inside your VM):

```bash
# Stop the VM
gcloud compute instances stop YOUR_VM_NAME --zone=YOUR_ZONE

# Grant full Cloud API access
gcloud compute instances set-service-account YOUR_VM_NAME \
  --zone=YOUR_ZONE \
  --service-account=YOUR_SERVICE_ACCOUNT_EMAIL \
  --scopes=https://www.googleapis.com/auth/cloud-platform

# Start it back up
gcloud compute instances start YOUR_VM_NAME --zone=YOUR_ZONE
```

To find your service account email: **GCP Console → Compute Engine → click your VM → Service accounts section**.

### 5. Grant the service account Storage access

Still in Cloud Shell:

```bash
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:YOUR_SERVICE_ACCOUNT_EMAIL" \
  --role="roles/storage.objectAdmin"
```

> `roles/storage.objectAdmin` allows full read/write on bucket objects. Use `roles/storage.objectViewer` for read-only.

### 6. Enable signed URL support

Signed URLs require IAM-based signing on a VM (no key file needed). Grant the service account permission to sign its own tokens, again from Cloud Shell:

```bash
gcloud iam service-accounts add-iam-policy-binding YOUR_SERVICE_ACCOUNT_EMAIL \
  --member="serviceAccount:YOUR_SERVICE_ACCOUNT_EMAIL" \
  --role="roles/iam.serviceAccountTokenCreator"
```

### 7. Run the demo

Back on your VM:

```bash
source .venv/bin/activate
export BUCKET_NAME="your-bucket-name"
python src/example.py
```

Expected output:
```
Uploaded string → gs://your-bucket/hello/world.txt
Objects in bucket:
  hello/world.txt
Content: Hello from GCP Starter! 🚀
Signed URL (expires in 30m): https://storage.googleapis.com/...
Deleted gs://your-bucket/hello/world.txt
Done.
```

---

## Common errors

| Error | Cause | Fix |
|---|---|---|
| `Request had insufficient authentication scopes` | VM created with default restricted scopes | Stop VM, update scopes to `cloud-platform`, restart (Step 4) |
| `403 Provided scope(s) are not authorized` | Same as above, hitting Storage API | Same fix |
| `you need a private key to sign credentials` | Signed URLs need IAM signing on a VM | Grant `serviceAccountTokenCreator` role (Step 6) |
| `gcloud` commands failing from inside the VM | VM's service account can't call IAM/Compute APIs | Run `gcloud` commands from Cloud Shell, not the VM SSH terminal |

---

## Running tests

No credentials needed — all GCS calls are mocked.

```bash
pip install pytest ruff
pytest tests/ -v
```

---

## Key functions (`src/storage.py`)

| Function | Description |
|---|---|
| `get_client()` | Returns an authenticated GCS client |
| `create_bucket()` | Creates a new bucket |
| `upload_file()` | Uploads a local file |
| `upload_string()` | Uploads a string directly |
| `download_file()` | Downloads to a local path |
| `download_as_string()` | Returns object content as string |
| `list_blobs()` | Lists objects (with optional prefix filter) |
| `delete_blob()` | Deletes an object |
| `generate_signed_url()` | Creates a temporary public URL (V4 signed) |