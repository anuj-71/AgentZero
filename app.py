from flask import Flask, request, jsonify, send_from_directory, Response
from flask_cors import CORS
from agents.swarm import run_swarm
import os
import requests

app = Flask(__name__, static_folder="frontend", static_url_path="")
CORS(app)

VOICE_CONFIG = {
    "nexus": {"primary": os.getenv("RESEARCH_VOICE_ID", "U2VUL94XlY3UYSlQvsxF"), "fallback": "Xb7hH8MSUJpSbSDYk0k2"},
    "research": {"primary": os.getenv("RESEARCH_VOICE_ID", "U2VUL94XlY3UYSlQvsxF"), "fallback": "Xb7hH8MSUJpSbSDYk0k2"},
    "aura": {"primary": os.getenv("FINANCE_VOICE_ID", "tJhWDBTSAveEOucKUtO0"), "fallback": "EXAVITQu4vr4xnSDxMaL"},
    "finance": {"primary": os.getenv("FINANCE_VOICE_ID", "tJhWDBTSAveEOucKUtO0"), "fallback": "EXAVITQu4vr4xnSDxMaL"},
    "echo": {"primary": os.getenv("MARKETING_VOICE_ID", "IwFADcBfc7Yo8KGhxTR5"), "fallback": "FGY2WhTYpPnrIDTdsKH5"},
    "marketing": {"primary": os.getenv("MARKETING_VOICE_ID", "IwFADcBfc7Yo8KGhxTR5"), "fallback": "FGY2WhTYpPnrIDTdsKH5"},
    "cog": {"primary": os.getenv("OPERATIONS_VOICE_ID", "kF8twSM38uBXVCgMToG0"), "fallback": "IKne3meq5aSn9XLyUdCD"},
    "operations": {"primary": os.getenv("OPERATIONS_VOICE_ID", "kF8twSM38uBXVCgMToG0"), "fallback": "IKne3meq5aSn9XLyUdCD"},
    "compliance": {"primary": os.getenv("OPERATIONS_VOICE_ID", "kF8twSM38uBXVCgMToG0"), "fallback": "IKne3meq5aSn9XLyUdCD"},
    "vex": {"primary": os.getenv("DEVIL_VOICE_ID", "J6QyEgpWnUhfFeU38ghG"), "fallback": "N2lVS1w4EtoT3dr4eOWO"},
    "credit": {"primary": os.getenv("DEVIL_VOICE_ID", "J6QyEgpWnUhfFeU38ghG"), "fallback": "N2lVS1w4EtoT3dr4eOWO"},
    "credit_risk": {"primary": os.getenv("DEVIL_VOICE_ID", "J6QyEgpWnUhfFeU38ghG"), "fallback": "N2lVS1w4EtoT3dr4eOWO"},
    "devils_advocate": {"primary": os.getenv("DEVIL_VOICE_ID", "J6QyEgpWnUhfFeU38ghG"), "fallback": "N2lVS1w4EtoT3dr4eOWO"},
    "prime": {"primary": os.getenv("CEO_VOICE_ID", "u8GDilEiJPUbRk87Lcqs"), "fallback": "JBFqnCBsd6RMkjVDRZzb"},
    "ceo": {"primary": os.getenv("CEO_VOICE_ID", "u8GDilEiJPUbRk87Lcqs"), "fallback": "JBFqnCBsd6RMkjVDRZzb"},
}


@app.route("/")
def index():
    if os.path.exists(os.path.join("ai_boardroom", "templates", "index.html")):
        return send_from_directory(os.path.join("ai_boardroom", "templates"), "index.html")
    return send_from_directory("frontend", "index.html")


@app.route("/terminal")
def terminal():
    return send_from_directory("frontend", "index.html")


@app.route("/api/tts", methods=["POST"])
def tts():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "").strip()
    agent = data.get("agent", "prime").lower()
    eleven_key = os.getenv("ELEVENLABS_API_KEY", "")
    model_id = os.getenv("ELEVENLABS_MODEL_ID", "eleven_flash_v2_5")

    if not text or not eleven_key:
        return jsonify({"error": "Missing text or ELEVENLABS_API_KEY"}), 400

    cfg = VOICE_CONFIG.get(agent, {"primary": os.getenv("CEO_VOICE_ID", "u8GDilEiJPUbRk87Lcqs"), "fallback": "JBFqnCBsd6RMkjVDRZzb"})
    primary_voice = cfg["primary"]
    fallback_voice = cfg["fallback"]

    # Truncate text if long to preserve response speed
    clean_text = text[:600]

    headers = {
        "xi-api-key": eleven_key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": clean_text,
        "model_id": model_id,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    # Attempt primary voice first
    try:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{primary_voice}"
        r = requests.post(url, json=payload, headers=headers, timeout=12)
        if r.status_code == 200:
            return Response(r.content, mimetype="audio/mpeg")
        
        # If primary returned 402/404, fallback to verified premade voice
        if r.status_code in (400, 402, 404):
            url_fallback = f"https://api.elevenlabs.io/v1/text-to-speech/{fallback_voice}"
            r_fallback = requests.post(url_fallback, json=payload, headers=headers, timeout=12)
            if r_fallback.status_code == 200:
                return Response(r_fallback.content, mimetype="audio/mpeg")
        
        return jsonify({"error": f"ElevenLabs API status {r.status_code}: {r.text}"}), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/run", methods=["POST"])
def run():
    data = request.get_json(silent=True) or {}
    business_problem = data.get("business_problem", "").strip()
    surprise = data.get("surprise", "").strip()
    if not business_problem:
        return jsonify({"error": "business_problem is required"}), 400
    try:
        result = run_swarm(business_problem, surprise)
        return jsonify({
            "trace": result.get("trace", []),
            "research": result.get("research_output", ""),
            "finance": result.get("finance_output", ""),
            "marketing": result.get("marketing_output", ""),
            "credit_risk": result.get("credit_risk_output", ""),
            "compliance": result.get("compliance_output", ""),
            "operations": result.get("compliance_output", ""),
            "devils_advocate": result.get("credit_risk_output", ""),
            "challenge": result.get("challenge_log", ""),
            "ceo_decision": result.get("ceo_decision", ""),
            "kpis": result.get("kpis", []),
            "revised_decision": result.get("revised_decision", ""),
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/testcases-report", methods=["GET"])
def testcases_report():
    import json
    report_path = os.path.join("data", "testcases_report.json")
    if os.path.exists(report_path):
        with open(report_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return jsonify(data)
    return jsonify({"error": "Report not found"}), 404


if __name__ == "__main__":
    app.run(debug=True, port=5000)



