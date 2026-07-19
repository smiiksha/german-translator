import tempfile
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.core.config import get_settings
from app.schemas.request_schemas import AnalyzeTextRequest
from app.schemas.response_schemas import AnalysisResponse
from app.services.grammar_service import analyze_grammar
from app.services.stt_service import transcribe_german

router = APIRouter(prefix="/analyze", tags=["grammar"])


@router.post("", response_model=AnalysisResponse)
def analyze_text(payload: AnalyzeTextRequest) -> AnalysisResponse:
    return analyze_grammar(payload.text)


@router.post("/audio", response_model=AnalysisResponse)
async def analyze_audio(audio: UploadFile = File(...)) -> AnalysisResponse:
    settings = get_settings()
    content = await audio.read()
    if not content:
        raise HTTPException(400, "The uploaded audio file is empty.")
    if len(content) > settings.max_upload_mb * 1024 * 1024:
        raise HTTPException(413, f"Audio must be smaller than {settings.max_upload_mb} MB.")
    suffix = Path(audio.filename or "audio.wav").suffix or ".wav"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as temp:
        temp.write(content)
        path = Path(temp.name)
    try:
        text = transcribe_german(path, settings.whisper_model)
        return analyze_grammar(text)
    except RuntimeError as exc:
        raise HTTPException(503, str(exc)) from exc
    finally:
        path.unlink(missing_ok=True)
