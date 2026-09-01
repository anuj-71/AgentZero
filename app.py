from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from agents.swarm import run_swarm
import os

app = Flask(__name__, static_folder="frontend", static_url_path="")
CORS(app)


@app.route("/")
def index():
    if os.path.exists(os.path.join("ai_boardroom", "templates", "index.html")):
        return send_from_directory(os.path.join("ai_boardroom", "templates"), "index.html")
    return send_from_directory("frontend", "index.html")


@app.route("/terminal")
def terminal():
    return send_from_directory("frontend", "index.html")


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
            "operations": result.get("operations_output", ""),
            "devils_advocate": result.get("devils_advocate_output", ""),
            "challenge": result.get("challenge_log", ""),
            "ceo_decision": result.get("ceo_decision", ""),
            "kpis": result.get("kpis", []),
            "revised_decision": result.get("revised_decision", ""),
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
