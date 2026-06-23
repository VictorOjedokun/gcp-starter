# GCP Cloud Storage Starter — Python

A clean Python starter for interacting with Google Cloud Storage (GCS). Upload, download, list, delete objects, and generate signed URLs.

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

## Setup

### 1. Clone & install

```bash
git clone https://github.com/<your-username>/gcp-storage-starter.git
cd gcp-storage-starter
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Authenticate with GCP

**Option A — Application Default Credentials (recommended for local dev)**
```bash
gcloud auth application-default login
```

**Option B — Service account key**
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your-key.json"
```
> ⚠️ Never commit `.json` key files. They are in `.gitignore`.

### 3. Set your bucket name

```bash
export BUCKET_NAME="your-bucket-name"
```

### 4. Run the demo

```bash
python src/example.py
```

---

## Running tests

No GCP credentials needed — all GCS calls are mocked.

```bash
pip install pytest ruff
pytest tests/ -v
```

---

## GitHub Actions CI

The included workflow (`.github/workflows/ci.yml`) runs on every push and PR to `main`:
- Lints with `ruff`
- Runs the test suite (mocked, no credentials required)

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
