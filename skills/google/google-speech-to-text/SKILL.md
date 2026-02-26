---
name: google-speech-to-text
description: "Transcribe audio files to text using Google Cloud Speech-to-Text API. Load when user mentions 'transcribe', 'speech to text', 'audio to text', 'transcribe audio', 'voice to text', 'transcription', or converting audio/recordings to text."
---

# Google Speech-to-Text

Transcribe audio files (MP3, WAV, FLAC, etc.) to text using Google Cloud Speech-to-Text API. Supports short files (sync) and long files (batch via Cloud Storage).

## Quick Start

### Transcribe a short audio file (≤60 seconds)

```bash
python3 00-system/skills/google/google-speech-to-text/scripts/transcribe_operations.py transcribe path/to/audio.mp3
```

### Transcribe with output to file

```bash
python3 00-system/skills/google/google-speech-to-text/scripts/transcribe_operations.py transcribe path/to/audio.mp3 --output transcript.txt
```

Output is automatically formatted into readable paragraphs. Use `--no-format` for raw output.

### Language (auto-detect default)

**Default:** Auto-detects German + English. Use `--language` to force a single language:

```bash
# Auto-detect (de-DE, en-US) - default
python3 ... transcribe audio.opus

# Force German
python3 ... transcribe audio.opus --language de-DE

# Force English
python3 ... transcribe audio.opus --language en-US
```

### Long audio – local file (no GCS): `transcribe-long`

For long **local** audio or **video** (e.g. MP4, Opus), use `transcribe-long`. It extracts audio (if video), splits into 60s chunks, transcribes each, and merges. **Requires ffmpeg** on PATH (or `FFMPEG_PATH`).

```bash
# Video (e.g. MP4) or long audio – German + English by default
python3 00-system/skills/google/google-speech-to-text/scripts/transcribe_operations.py transcribe-long /path/to/file.mp4 --output transcript.txt
```

Use the project’s venv if you installed `google-cloud-speech` there:

```bash
.venv-speech/bin/python3 00-system/skills/google/google-speech-to-text/scripts/transcribe_operations.py transcribe-long /path/to/file.mp4 --output transcript.txt
```

### Long audio – GCS batch (up to 8 hours)

For files >60 seconds **without** local chunking, upload to Google Cloud Storage and use batch mode:

```bash
# 1. Upload to GCS (gsutil or your bucket)
gcloud storage cp audio.mp3 gs://your-bucket/audio.mp3

# 2. Batch transcribe
python3 00-system/skills/google/google-speech-to-text/scripts/transcribe_operations.py transcribe-batch gs://your-bucket/audio.mp3 --output transcript.txt
```

## Pre-Flight Check

Speech-to-Text uses **Google Cloud** (not OAuth Workspace). It requires Application Default Credentials.

```bash
# Check if configured
python3 00-system/skills/google/google-speech-to-text/scripts/transcribe_operations.py check
```

**If not configured:**
```bash
gcloud auth application-default login
```

Then set `GOOGLE_CLOUD_PROJECT` in `.env` or `export GOOGLE_CLOUD_PROJECT=your-project-id`.

## Setup

### 1. Enable the API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project (or create one)
3. Enable **Speech-to-Text API**: [Enable API](https://console.cloud.google.com/flows/enableapi?apiid=speech.googleapis.com)
4. Ensure billing is enabled (free tier: $300 credits for new accounts)

### 2. Authenticate

```bash
# Option A: User credentials (recommended for local use)
gcloud auth application-default login

# Option B: Service account (for automation)
gcloud iam service-accounts create speech-transcribe --display-name "Speech Transcription"
# ... grant role, then:
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
```

### 3. Set project ID

Add to `.env` at Beam Next root:
```
GOOGLE_CLOUD_PROJECT=your-project-id
```

Or use GOOGLE_PROJECT_ID from your existing Google setup (same project can host both Workspace and Speech APIs).

## Supported formats

| Format | Sync | Batch |
|--------|------|-------|
| WAV, FLAC, LINEAR16 | ✅ | ✅ |
| MP3, OGG, AMR | ✅ (auto-decode) | ✅ |
| WebM, Opus | ✅ | ✅ |

## Model options

- `--model long`: Best for long-form (meetings, podcasts) - default for batch
- `--model short`: Default for sync, optimized for short utterances
- `--model latest_long`: Latest long-form model (Chirp 3)

## API Reference

| Mode | Limit | Use case |
|------|-------|----------|
| Sync | ≤60 sec | Quick clips, voice notes |
| Batch | ≤480 min | Meetings, podcasts, interviews |

**Note:** Google Cloud Speech-to-Text is a separate API from Google Workspace (Gmail, Docs). It uses Application Default Credentials, not OAuth tokens. You can use the same Google Cloud project.

## Additional resources

- For setup: [references/setup-guide.md](references/setup-guide.md)
- [Google Cloud Speech-to-Text docs](https://cloud.google.com/speech-to-text/docs)
