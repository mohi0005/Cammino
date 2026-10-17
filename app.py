import json, os
from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai import types

app = Flask(__name__)
MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", ""))

SYSTEM = (
    "You are Cammino, a practical career guidance agent for skilled young people "
    "in Tier-2/3 Indian cities. Be realistic, specific and encouraging. Prefer roles "
    "reachable via remote work or nearby cities. Never invent salary figures. "
    "Reply ONLY with JSON matching this schema: "
    '{"summary": str, "job_paths": [{"title": str, "why_fit": str, "demand_note": str}], '
    '"skill_gaps": [str], "roadmap": [{"week": int, "focus": str, "tasks": [str]}], '
    '"resume_tips": [str]}. Give 3 job_paths and a 4-week roadmap.'
)

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/guidance")
def guidance():
    d = request.get_json(force=True)
    skills = (d.get("skills") or "").strip()
    if not skills:
        return jsonify(error="Please enter at least one skill."), 400
    prompt = (
        f"Education: {d.get('education','')}\nSkills: {skills}\n"
        f"Interests: {d.get('interests','')}\nCity: {d.get('city','')}\n"
        f"Reply in: {d.get('language','English')} (keep JSON keys in English)."
    )
    try:
        r = client.models.generate_content(
            model=MODEL, contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM, response_mime_type="application/json"),
        )
        return jsonify(json.loads(r.text))
    except Exception as e:
        return jsonify(error=f"AI service error: {e}"), 502

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
