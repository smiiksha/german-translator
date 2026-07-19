# German Grammar & Context API

A FastAPI service that accepts German text (and optionally audio), returns a learner-friendly English translation, grammar corrections, explanations, and a CEFR estimate.

It works immediately in **offline mode** with a small, deterministic set of German grammar rules. Add an `OPENAI_API_KEY` to use LLM-based structured analysis. Audio transcription is optional and uses local Whisper.

## Features

- `POST /api/v1/analyze` — analyze German text
- `POST /api/v1/analyze/audio` — transcribe then analyze German audio
- `GET /api/v1/health` — health check
- Input/output validation with Pydantic
- Swagger UI at `/docs`
- Dockerfile included

## Run in VS Code (Windows)

1. Extract the ZIP, then open the `german-grammar-api` folder in VS Code: **File → Open Folder**.
2. Install the **Python** extension if VS Code asks.
3. Open **Terminal → New Terminal** and run:

   ```powershell
   py -3.11 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   Copy-Item .env.example .env
   uvicorn app.main:app --reload
   ```

   If PowerShell blocks activation, run this once in that terminal and repeat the activation command:

   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   ```

4. Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs). Expand `POST /api/v1/analyze`, choose **Try it out**, and send:

   ```json
   {"text": "Ich gehe mit den Mann."}
   ```

5. Stop the server with `Ctrl+C`.

### Enable OpenAI analysis (optional)

Edit `.env` and set `OPENAI_API_KEY=your_key`. Restart the server. The app then requests strict JSON from the configured model; if that request fails it safely uses offline rules.

### Enable audio analysis (optional)

Install the audio dependencies and ensure [FFmpeg](https://ffmpeg.org/download.html) is available on your PATH:

```powershell
pip install -r requirements-audio.txt
```

Then use `POST /api/v1/analyze/audio` in Swagger to upload a German audio file. Whisper downloads its selected model on first use.

## API example

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/api/v1/analyze `
  -ContentType 'application/json' `
  -Body '{"text":"Ich gehe mit den Mann."}'
```

Expected core result:

```json
{
  "is_correct": false,
  "corrected_sentence": "Ich gehe mit dem Mann.",
  "analysis_provider": "heuristic"
}
```

## Test

```powershell
pip install pytest httpx
pytest
```

## Project layout

```
app/
  core/       # environment configuration
  routes/     # HTTP endpoints
  schemas/    # request and response validation
  services/   # translation, grammar, and speech services
tests/
```
