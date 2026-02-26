#!/usr/bin/env python3
"""
Google Cloud Speech-to-Text Transcription

Transcribe audio files to text. Supports:
- Sync: short files up to 60 seconds (local files)
- Batch: long files up to 480 minutes (GCS URIs)

Requires: pip install google-cloud-speech
Auth: gcloud auth application-default login
"""

import argparse
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path


def find_beam_next_root():
    """Find Beam Next root by looking for CLAUDE.md or .env."""
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "CLAUDE.md").exists() or (parent / ".env").exists():
            return parent
    return Path.cwd()


def load_env():
    """Load .env file into environment."""
    beam_next_root = find_beam_next_root()
    env_path = beam_next_root / ".env"
    if env_path.exists():
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ.setdefault(key.strip(), value.strip())


load_env()


def get_project_id():
    """Get Google Cloud project ID from env."""
    return os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GOOGLE_PROJECT_ID")


def cmd_check():
    """Verify Speech-to-Text is configured."""
    project_id = get_project_id()
    if not project_id:
        print("ERROR: GOOGLE_CLOUD_PROJECT or GOOGLE_PROJECT_ID not set")
        print("Add to .env: GOOGLE_CLOUD_PROJECT=your-project-id")
        return 2

    try:
        from google.cloud.speech_v2 import SpeechClient

        client = SpeechClient()
        # Quick validation - list recognize request would fail if not configured
        print("OK: Speech-to-Text configured")
        print(f"  Project: {project_id}")
        print("  Auth: Application Default Credentials")
        return 0
    except ImportError as e:
        print("ERROR: google-cloud-speech not installed")
        print("Run: pip install google-cloud-speech")
        return 2
    except Exception as e:
        if "Could not automatically determine credentials" in str(e) or "403" in str(e):
            print("ERROR: Not authenticated. Run: gcloud auth application-default login")
        else:
            print(f"ERROR: {e}")
        return 2


# Auto-detect languages (API picks best fit, max 3). Covers German + English.
DEFAULT_LANGUAGE_CODES = ["de-DE", "en-US"]


# Phrases that often start new sentences (German/English) - break before these
_SENTENCE_STARTERS = re.compile(
    r'\s+(und dann |und ich |und das |dann |also |aber |ja und |so und |ich habe |ich bin |ich war |ich dachte )',
    re.IGNORECASE
)


def format_transcript(raw: str) -> str:
    """Format raw transcript: single newlines, add periods at sentence breaks."""
    text = raw.strip()
    if not text:
        return text
    # Split on existing sentence boundaries (. ! ?)
    sentences = re.split(r'(?<=[.!?])\s+', text)
    sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 10]
    # Use smart split if no punctuation or only one very long "sentence"
    if not sentences or (len(sentences) == 1 and len(sentences[0]) > 200):
        lines = []
        pos = 0
        while pos < len(text):
            chunk = text[pos : pos + 130]
            match = _SENTENCE_STARTERS.search(chunk)
            # Prefer break before sentence starter if it's 25-110 chars in
            if match and 25 < match.start() < 110:
                break_at = pos + match.start()
                line = text[pos:break_at].strip()
                pos = break_at
            else:
                # Break at word boundary near 100 chars
                break_at = min(pos + 100, len(text))
                if break_at < len(text):
                    space = text.rfind(" ", pos, break_at + 25)
                    if space > pos + 50:
                        break_at = space
                line = text[pos:break_at].strip()
                pos = break_at
            if line:
                if not line.endswith(('.', '!', '?')):
                    line = line + "."
                lines.append(line)
        return "\n".join(lines)
    # Already has punctuation: one sentence per line, ensure period at end
    result = []
    for s in sentences:
        s = s.strip()
        if s and not s.endswith(('.', '!', '?')):
            s = s + "."
        if s:
            result.append(s)
    return "\n".join(result)


def transcribe_sync(audio_path: str, language_codes: list[str] | None = None, model: str = "long", format_output: bool = True) -> str:
    """Transcribe short audio file (≤60 sec) synchronously."""
    from google.cloud.speech_v2 import SpeechClient
    from google.cloud.speech_v2.types import cloud_speech

    project_id = get_project_id()
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT not set")

    codes = language_codes or DEFAULT_LANGUAGE_CODES

    with open(audio_path, "rb") as f:
        content = f.read()

    client = SpeechClient()
    config = cloud_speech.RecognitionConfig(
        auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
        language_codes=codes,
        model=model,
    )
    request = cloud_speech.RecognizeRequest(
        recognizer=f"projects/{project_id}/locations/global/recognizers/_",
        config=config,
        content=content,
    )
    response = client.recognize(request=request)

    transcripts = []
    for result in response.results:
        if result.alternatives:
            transcripts.append(result.alternatives[0].transcript)
    raw = "\n".join(transcripts)
    return raw if not format_output else format_transcript(raw)


def find_ffmpeg() -> str:
    """Return path to ffmpeg binary (required for video extraction and chunking)."""
    if os.environ.get("FFMPEG_PATH"):
        p = os.environ.get("FFMPEG_PATH").strip()
        if os.path.isfile(p) and os.access(p, os.X_OK):
            return p
    for path in ("ffmpeg", "/opt/homebrew/bin/ffmpeg", "/usr/local/bin/ffmpeg"):
        if path == "ffmpeg":
            try:
                subprocess.run([path, "-version"], capture_output=True, check=True, timeout=5, env=os.environ)
                return path
            except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
                continue
        if os.path.isfile(path) and os.access(path, os.X_OK):
            return path
    raise FileNotFoundError("ffmpeg not found. Install with: brew install ffmpeg (or set FFMPEG_PATH)")


def extract_audio_from_video(video_path: str, out_flac: str) -> None:
    """Extract 16kHz mono FLAC from video (Speech-to-Text friendly)."""
    ffmpeg = find_ffmpeg()
    env = os.environ.copy()
    env.setdefault("PATH", "/usr/local/bin:/opt/homebrew/bin:" + env.get("PATH", ""))
    subprocess.run(
        [ffmpeg, "-y", "-i", video_path, "-vn", "-acodec", "flac", "-ar", "16000", "-ac", "1", out_flac],
        check=True,
        capture_output=True,
        timeout=600,
        env=env,
    )


def split_audio_into_chunks(flac_path: str, segment_sec: int, temp_dir: Path) -> list[Path]:
    """Split FLAC into segment_sec-second chunks. Returns list of chunk paths."""
    ffmpeg = find_ffmpeg()
    env = os.environ.copy()
    env.setdefault("PATH", "/usr/local/bin:/opt/homebrew/bin:" + env.get("PATH", ""))
    out_pattern = str(temp_dir / "chunk_%04d.flac")
    subprocess.run(
        [ffmpeg, "-y", "-i", flac_path, "-f", "segment", "-segment_time", str(segment_sec), "-c", "copy", out_pattern],
        check=True,
        capture_output=True,
        timeout=600,
        env=env,
    )
    return sorted(temp_dir.glob("chunk_*.flac"))


def transcribe_long_local(
    audio_or_video_path: str,
    language_codes: list[str] | None = None,
    model: str = "long",
    format_output: bool = True,
    segment_sec: int = 60,
) -> str:
    """Transcribe a long local file (video or audio) by chunking and sync API. No GCS required."""
    path = Path(audio_or_video_path)
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")
    video_extensions = {".mp4", ".webm", ".mov", ".mkv", ".m4a"}
    is_video = path.suffix.lower() in video_extensions
    with tempfile.TemporaryDirectory(prefix="transcribe_long_") as tmp:
        temp_dir = Path(tmp)
        if is_video:
            flac_path = str(temp_dir / "audio.flac")
            print("Extracting audio from video...")
            extract_audio_from_video(str(path.resolve()), flac_path)
        else:
            flac_path = str(path.resolve())
            # For non-video we still need FLAC for consistent chunking; if already FLAC/WAV, copy to temp and chunk
            if path.suffix.lower() not in {".flac", ".wav"}:
                flac_path = str(temp_dir / "audio.flac")
                ffmpeg = find_ffmpeg()
                env = os.environ.copy()
                env.setdefault("PATH", "/usr/local/bin:/opt/homebrew/bin:" + env.get("PATH", ""))
                subprocess.run(
                    [ffmpeg, "-y", "-i", str(path.resolve()), "-acodec", "flac", "-ar", "16000", "-ac", "1", flac_path],
                    check=True,
                    capture_output=True,
                    timeout=600,
                    env=env,
                )
        print("Splitting into segments...")
        chunks = split_audio_into_chunks(flac_path, segment_sec, temp_dir)
        if not chunks:
            raise RuntimeError("No chunks produced")
        print(f"Transcribing {len(chunks)} segments (this may take a few minutes)...")
        parts = []
        for i, chunk_path in enumerate(chunks):
            try:
                text = transcribe_sync(str(chunk_path), language_codes, model, format_output=False)
                if text.strip():
                    parts.append(text.strip())
            except Exception as e:
                print(f"Warning: segment {i + 1} failed: {e}", file=sys.stderr)
        raw = "\n\n".join(parts)
        return raw if not format_output else format_transcript(raw)


def transcribe_batch(gcs_uri: str, language_codes: list[str] | None = None, model: str = "long", format_output: bool = True) -> str:
    """Transcribe long audio from GCS (async batch)."""
    from google.cloud.speech_v2 import SpeechClient
    from google.cloud.speech_v2.types import cloud_speech

    project_id = get_project_id()
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT not set")

    if not gcs_uri.startswith("gs://"):
        raise ValueError("Batch mode requires GCS URI (gs://bucket/path)")

    codes = language_codes or DEFAULT_LANGUAGE_CODES

    client = SpeechClient()
    config = cloud_speech.RecognitionConfig(
        auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
        language_codes=codes,
        model=model,
    )
    request = cloud_speech.BatchRecognizeRequest(
        recognizer=f"projects/{project_id}/locations/global/recognizers/_",
        config=config,
        files=[cloud_speech.BatchRecognizeFileMetadata(uri=gcs_uri)],
        recognition_output_config=cloud_speech.RecognitionOutputConfig(
            inline_response_config=cloud_speech.InlineOutputConfig(),
        ),
    )
    operation = client.batch_recognize(request=request)

    print("Transcribing (this may take several minutes for long files)...")
    response = operation.result(timeout=3600)  # 1 hour max wait

    transcripts = []
    if response.results and gcs_uri in response.results:
        file_result = response.results[gcs_uri]
        if hasattr(file_result, "transcript") and file_result.transcript:
            for result in file_result.transcript.results:
                if result.alternatives:
                    transcripts.append(result.alternatives[0].transcript)

    raw = "\n".join(transcripts)
    return raw if not format_output else format_transcript(raw)


def main():
    parser = argparse.ArgumentParser(description="Google Speech-to-Text transcription")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # check
    subparsers.add_parser("check", help="Verify Speech-to-Text is configured")

    # transcribe (sync)
    trans_parser = subparsers.add_parser("transcribe", help="Transcribe short audio (≤60 sec)")
    trans_parser.add_argument("audio", help="Path to audio file")
    trans_parser.add_argument("--output", "-o", help="Output file path")
    trans_parser.add_argument(
        "--language", "-l",
        help="Language code (e.g. de-DE, en-US). Default: auto-detect (de-DE, en-US)"
    )
    trans_parser.add_argument("--model", "-m", default="long", help="Model: short, long, latest_long")
    trans_parser.add_argument("--no-format", action="store_true", help="Skip paragraph formatting")

    # transcribe-long (local long file: extract + chunk + sync + merge; no GCS)
    long_parser = subparsers.add_parser("transcribe-long", help="Transcribe long local audio/video (extract + chunk + merge). Requires ffmpeg.")
    long_parser.add_argument("audio_or_video", help="Path to audio or video file (e.g. .mp4, .opus, .flac)")
    long_parser.add_argument("--output", "-o", help="Output file path")
    long_parser.add_argument("--language", "-l", help="Language code (e.g. de-DE, en-US). Default: de-DE + en-US")
    long_parser.add_argument("--model", "-m", default="long", help="Model: short, long, latest_long")
    long_parser.add_argument("--no-format", action="store_true", help="Skip paragraph formatting")
    long_parser.add_argument("--segment-sec", type=int, default=60, help="Chunk length in seconds (default 60, max for sync API)")

    # transcribe-batch
    batch_parser = subparsers.add_parser("transcribe-batch", help="Transcribe long audio from GCS")
    batch_parser.add_argument("gcs_uri", help="GCS URI: gs://bucket/path/to/audio.mp3")
    batch_parser.add_argument("--output", "-o", help="Output file path")
    batch_parser.add_argument(
        "--language", "-l",
        help="Language code (e.g. de-DE, en-US). Default: auto-detect (de-DE, en-US)"
    )
    batch_parser.add_argument("--model", "-m", default="long", help="Model: long (chirp_3 needs us/eu location)")
    batch_parser.add_argument("--no-format", action="store_true", help="Skip paragraph formatting")

    args = parser.parse_args()

    if args.command == "check":
        return cmd_check()

    if args.command == "transcribe":
        lang_codes = [args.language] if args.language else None
        if lang_codes:
            print(f"Using language: {args.language}")
        else:
            print(f"Auto-detecting language (de-DE, en-US). Override with --language de-DE")
        try:
            result = transcribe_sync(args.audio, lang_codes, args.model, format_output=not args.no_format)
        except Exception as e:
            print(f"ERROR: {e}")
            return 1
        if args.output:
            Path(args.output).write_text(result, encoding="utf-8")
            print(f"Saved to {args.output}")
        else:
            print(result)
        return 0

    if args.command == "transcribe-long":
        lang_codes = [args.language] if args.language else None
        if lang_codes:
            print(f"Using language: {args.language}")
        else:
            print("Auto-detecting language (de-DE, en-US). Override with --language de-DE")
        try:
            result = transcribe_long_local(
                args.audio_or_video,
                lang_codes,
                args.model,
                format_output=not args.no_format,
                segment_sec=args.segment_sec,
            )
        except FileNotFoundError as e:
            print(f"ERROR: {e}")
            return 1
        except Exception as e:
            print(f"ERROR: {e}")
            return 1
        if args.output:
            out_path = Path(args.output)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(result, encoding="utf-8")
            print(f"Saved to {args.output}")
        else:
            print(result)
        return 0

    if args.command == "transcribe-batch":
        lang_codes = [args.language] if args.language else None
        if lang_codes:
            print(f"Using language: {args.language}")
        else:
            print(f"Auto-detecting language (de-DE, en-US). Override with --language de-DE")
        try:
            result = transcribe_batch(args.gcs_uri, lang_codes, args.model, format_output=not args.no_format)
        except Exception as e:
            print(f"ERROR: {e}")
            return 1
        if args.output:
            Path(args.output).write_text(result, encoding="utf-8")
            print(f"Saved to {args.output}")
        else:
            print(result)
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
