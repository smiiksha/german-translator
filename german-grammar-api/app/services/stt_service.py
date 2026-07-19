from pathlib import Path


def transcribe_german(audio_path: Path, model_name: str = "base") -> str:
    """Transcribe audio locally with Whisper (installed with the optional audio extras)."""
    try:
        import whisper
    except ImportError as exc:
        raise RuntimeError("Audio support is not installed. Run: pip install -r requirements-audio.txt") from exc
    model = whisper.load_model(model_name)
    return model.transcribe(str(audio_path), language="de", fp16=False)["text"].strip()
