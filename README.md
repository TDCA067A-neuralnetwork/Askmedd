# AskMed — Clinical Question Answering System

Educational final-year project prototype. The application accepts medical/clinical/healthcare questions, blocks common prompt-injection attempts, rejects unrelated questions before the LLM, detects possible emergency wording, and can call an OpenAI-compatible hosted medical LLM endpoint.

## Run locally

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`.

## Vercel environment variables

Set these in Vercel Project Settings → Environment Variables:

- `HF_BASE_URL` — your OpenAI-compatible Hugging Face endpoint base URL
- `HF_TOKEN` — your Hugging Face access token
- `MEDICAL_MODEL` — model name supported by that endpoint

Do not put the token in source code or GitHub.

## Tests

```bash
pytest -q
```

## Important

This is an educational prototype, not a clinically validated medical device. It must not be presented as a doctor or as a replacement for professional care.
