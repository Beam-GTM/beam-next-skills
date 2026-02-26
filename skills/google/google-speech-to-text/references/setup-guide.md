# Google Speech-to-Text Setup Guide

Speech-to-Text uses **Google Cloud** authentication (Application Default Credentials), not OAuth. It can share the same Google Cloud project as your Workspace integrations.

## Prerequisites

- Google Cloud project (can reuse GOOGLE_PROJECT_ID from .env)
- Billing enabled (new accounts get $300 free credits)
- gcloud CLI installed

## Step 1: Enable the API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project (or create one)
3. Go to [Enable Speech-to-Text API](https://console.cloud.google.com/flows/enableapi?apiid=speech.googleapis.com)
4. Click Enable

## Step 2: Install the client library

```bash
pip install google-cloud-speech
```

## Step 3: Authenticate

**Option A: User credentials (local development)**

```bash
gcloud auth application-default login
```

This opens a browser to sign in. Credentials are stored in `~/.config/gcloud/application_default_credentials.json`.

**Option B: Service account (automation)**

1. Create a service account in Cloud Console
2. Grant role: Cloud Speech Administrator (or Speech-to-Text User)
3. Create a JSON key and download it
4. Set: `export GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json`

## Step 4: Set project ID

Add to `.env` at Beam Next root:

```
GOOGLE_CLOUD_PROJECT=your-project-id
```

Or use `GOOGLE_PROJECT_ID` if you already have it for Google Workspace (same project works for both).

## Step 5: Verify

```bash
python3 00-system/skills/google/google-speech-to-text/scripts/transcribe_operations.py check
```

## Long audio (batch mode)

For files >60 seconds:

1. Create a Cloud Storage bucket (or use existing)
2. Upload audio: `gcloud storage cp audio.mp3 gs://your-bucket/`
3. Ensure the Speech-to-Text service account has read access to the bucket
4. Run: `transcribe_operations.py transcribe-batch gs://your-bucket/audio.mp3`

## Troubleshooting

| Error | Solution |
|-------|----------|
| "Could not automatically determine credentials" | Run `gcloud auth application-default login` |
| "403 Permission Denied" | Enable Speech-to-Text API, check IAM roles |
| "GOOGLE_CLOUD_PROJECT not set" | Add to .env or export |
| "google-cloud-speech not installed" | `pip install google-cloud-speech` |
