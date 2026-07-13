# 🇩🇪 Multilingual Grammar & Context API

> A production-oriented NLP backend that analyzes German text or speech, detects grammatical mistakes using an LLM, and returns structured, learner-friendly feedback.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![Whisper](https://img.shields.io/badge/OpenAI-Whisper-black)
![LLM](https://img.shields.io/badge/LLM-Claude%20%7C%20GPT-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## 📖 Overview

Learning German is difficult because grammar feedback is often either:

- too generic,
- limited to simple spell checking,
- or doesn't explain *why* something is incorrect.

This project solves that problem by building a complete NLP pipeline that accepts **German text or speech**, analyzes grammar using an LLM, and returns **structured explanations** that help learners understand their mistakes.

Instead of simply correcting a sentence, the API identifies:

- adjective declension errors
- incorrect case usage
- verb placement mistakes
- article agreement
- verb conjugation issues

while also generating an English translation for reference.

---

# ✨ Features

- 🎙 German speech → text transcription (Whisper)
- 🇩🇪 German → English translation
- 🤖 LLM-powered grammar evaluation
- 📚 Rule-specific explanations
- 📄 Structured JSON responses
- 🎯 CEFR difficulty estimation (A1–C2)
- ⚡ FastAPI REST API
- 🧩 Modular service-based architecture
- 🐳 Docker-ready deployment

---

# 🏗 System Architecture

```
              Client
        (Text / Audio Input)
                 │
                 ▼
        FastAPI Request Router
                 │
     ┌───────────┴───────────┐
     │                       │
 Text Input             Audio Upload
     │                       │
     │               Audio Preprocessing
     │                       │
     │                 Whisper STT
     │                       │
     └──────────► German Text ◄──────────┘
                    │
                    ▼
         Translation Service
          (German → English)
                    │
                    ▼
        Grammar Evaluation Service
          (LLM Prompt Pipeline)
                    │
                    ▼
          Structured JSON Output
                    │
                    ▼
                 Client
```

---

# 🛠 Tech Stack

| Layer | Technology |
|---------|------------|
| Backend | FastAPI |
| Speech-to-Text | OpenAI Whisper |
| Translation | Helsinki-NLP / DeepL |
| Grammar Analysis | Claude / GPT |
| Validation | Pydantic |
| Audio Processing | pydub + ffmpeg |
| Deployment | Railway / Render |
| Environment | python-dotenv |

---

# 📂 Project Structure

```
german-grammar-api/

app/
│
├── routes/
│     grammar.py
│     health.py
│
├── services/
│     stt_service.py
│     translation_service.py
│     grammar_service.py
│
├── schemas/
│     request_schemas.py
│     response_schemas.py
│
├── utils/
│     audio_utils.py
│     prompt_builder.py
│
├── core/
│     config.py
│     exceptions.py
│
└── main.py

tests/

Dockerfile
README.md
requirements.txt
.env.example
```

---

# 🔄 Request Flow

### Text

```
Text
 ↓
Translation
 ↓
Grammar Analysis
 ↓
Structured Response
```

### Audio

```
Audio Upload
 ↓
Preprocessing
 ↓
Speech-to-Text
 ↓
Translation
 ↓
Grammar Analysis
 ↓
Structured Response
```

---

# 📌 API Endpoint

## POST `/api/v1/analyze`

Accepts either:

- German text
- German audio file

---

### Example Request

#### Text

```json
{
  "text": "Ich gehe mit den Mann."
}
```

---

### Example Response

```json
{
  "original_german": "Ich gehe mit den Mann.",

  "english_translation": "I am going with the man.",

  "is_correct": false,

  "errors": [
    {
      "type": "case_error",

      "original_fragment": "den Mann",

      "corrected_fragment": "dem Mann",

      "rule_violated": "Dative after 'mit'",

      "explanation": "The preposition 'mit' always requires the dative case."
    }
  ],

  "corrected_sentence": "Ich gehe mit dem Mann.",

  "difficulty_level": "A2",

  "overall_explanation": "The sentence contains a dative case error after the preposition 'mit'."
}
```

---

# 🧠 Grammar Rules Checked

The LLM is explicitly prompted to detect:

- Adjective Declension
- Case Usage
- Article Agreement
- Verb Placement
- Verb Conjugation
- Word Order
- Other contextual grammar issues

Rather than asking the model to "check grammar", the prompt instructs it to evaluate specific German grammar rules and return a strictly structured JSON response.

---

# ⚙️ Design Principles

This project follows a service-oriented architecture.

- Routes only receive requests.
- Services contain business logic.
- Schemas validate all inputs and outputs.
- Utilities handle reusable functionality.
- Configuration is centralized.

This separation keeps the backend scalable and easy to maintain.

---

# 🔒 Security

- Environment variables stored in `.env`
- API keys never committed
- Input validation using Pydantic
- Temporary audio files automatically deleted after processing
- Structured JSON validation before returning responses

---

# 🚀 Running Locally

Clone the repository

```bash
git clone https://github.com/yourusername/german-grammar-api.git
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env`

```env
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...
DEEPL_API_KEY=...
```

Run

```bash
uvicorn app.main:app --reload
```

Visit

```
http://127.0.0.1:8000/docs
```

for the interactive Swagger documentation.

---

# 🌍 Deployment

The API is designed for deployment on platforms such as:

- Railway
- Render
- Fly.io

Deployment includes:

- Docker support
- Environment-based configuration
- Health endpoint
- Automatic API documentation

---

# 🎯 Future Improvements

- Streaming audio transcription
- User authentication
- Error history dashboard
- Grammar statistics
- Conversation context memory
- Vocabulary suggestions
- Pronunciation scoring
- Batch document analysis
- RAG using German grammar reference material
- Frontend dashboard built with React or Next.js

---

# 📈 Resume Highlights

**Multilingual Grammar & Context API**

- Designed a modular FastAPI backend for multilingual grammar evaluation.
- Built an end-to-end NLP pipeline integrating speech recognition, machine translation, and LLM-based grammar analysis.
- Engineered structured prompting to detect German grammar errors including adjective declension, case usage, and verb placement.
- Implemented schema validation, secure API handling, and production-ready deployment architecture.

---

# 🤝 Contributing

Contributions, suggestions, and issue reports are welcome.

Feel free to fork the repository and submit a pull request.

---

# 📄 License

This project is licensed under the MIT License.

---

## ⭐ Why This Project?

Unlike traditional grammar checkers, this project combines speech recognition, machine translation, prompt engineering, and backend architecture into a single production-style NLP service.

The focus is not only on correcting German sentences, but also on providing structured, explainable feedback that helps language learners understand *why* a correction is needed.
