# Cammino AI
Cammino ("path" in Italian) is a career guidance web app for skilled youth in Tier-2/3 Indian cities. Supports **UN SDG 8: Decent Work and Economic Growth**.

Enter your education, skills, interests and city. The agent (Gemini API) returns best-fit job paths, skill gaps, a 4-week learning roadmap and resume tips, in English, Hindi, Telugu or Urdu.

## Stack
Python, Flask, Google Gemini API (`google-genai`), gunicorn. Deployable on Railway or Google Cloud Run.

## Run locally
```
pip install -r requirements.txt
export GEMINI_API_KEY=your_key      # Windows: set GEMINI_API_KEY=your_key
python app.py                       # http://localhost:8080
```
Optional: `GEMINI_MODEL` (default `gemini-2.5-flash`).

## Deploy (Railway)
Push to GitHub, create a Railway project from the repo, add `GEMINI_API_KEY` as a variable. The `Procfile` handles the start command.

## Endpoints
`GET /` UI, `GET /health`, `POST /api/guidance` (JSON: education, skills, interests, city, language).

Guidance is AI-generated and indicative, not a guarantee of employment.
