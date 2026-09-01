# Agentic Swarm - AI Boardroom
### Team: Agent Zero
**Members:** Anuj Agarwal · Palak Malhotra · Pranjal Rai

---

## Challenge Selected
Build a multi-agent AI system that simulates a business boardroom. Given any business problem, a swarm of specialized AI agents analyses, debates, challenges assumptions, and reaches a structured CEO decision - then adapts when surprise events are injected.

## Solution Summary
Agentic Swarm is a LangGraph-powered multi-agent decision engine with a web interface. Six specialized agents run in a structured boardroom protocol - Analyse, Share, Challenge, Compare, Decide - and produce a CEO directive with evidence, rejected alternatives, risks, implementation steps, and measurable KPIs. A Surprise Round forces the swarm to re-evaluate the decision against unexpected market events in real time.

---

## Agent List

| Agent | Role | Input | Output |
|-------|------|-------|--------|
| Research Agent (NEXUS) | Market analysis - opportunity, competitors, risks, target customers | Business problem statement | 4-point research brief forwarded to Finance, Marketing, Operations |
| Finance Agent | Cost, revenue, break-even, financial risks | Business problem + Research output | RECOMMEND or DO NOT RECOMMEND with key financial reason |
| Marketing Agent (ECHO) | Target segment, positioning, acquisition channels, marketing risk | Business problem + Research output | GO or NO-GO with channel strategy |
| Challenge Agent (VEX) | Identifies conflict between Finance and Marketing | Finance output + Marketing output | Named conflict between agents + CEO resolution proposal |
| Operations Agent (AURA) | Feasibility, execution risks, regulatory, resource requirements | Business problem + all dept outputs | FEASIBLE or NOT FEASIBLE + biggest operational risk |
| Devil's Advocate (COG) | Challenges the most dangerous assumption across all agents | All department outputs | ASSUMPTION CHALLENGED + WHY IT COULD BE WRONG + WHAT CEO MUST VERIFY |
| CEO Agent (PRIME) | Synthesizes all agent inputs into final executive directive | All 6 agent outputs | DECISION + EVIDENCE USED + REJECTED ALTERNATIVE + KEY RISKS + IMPLEMENTATION + 3 KPIs |
| Surprise Agent | Re-evaluates CEO decision against a new market event | CEO decision + surprise event | WHAT CHANGED + WHAT STAYS THE SAME + REVISED DECISION + UPDATED KPIs |

---

## Installation

**Requirements:** Python 3.10+, pip, Google Gemini API key

**Step 1 - Clone the repo:**
```bash
git clone https://github.com/anuj-71/AgentZero.git
cd AgentZero
```

**Step 2 - Install dependencies:**
```bash
pip install flask flask-cors langgraph langchain-core langchain-google-genai python-dotenv
```

**Step 3 - Create .env file in project root:**
```env
GOOGLE_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3.1-flash-lite
```

**Step 4 - Run the server:**
```bash
python app.py
```

**Step 5 - Open in browser:**
```
http://127.0.0.1:5000
```

**Step 6 - Test backend only (optional):**
```bash
python agents/swarm.py "Your business problem here"
```

**Step 7 - Test with surprise round:**
```bash
python agents/swarm.py "Your business problem" "Your surprise event"
```

---

## Models, Frameworks and External Services

| Component | Details |
|-----------|---------|
| LLM | Google Gemini 3.1 Flash Lite via Gemini API |
| Agent Framework | LangGraph 1.x - StateGraph with fan-out/fan-in topology |
| LLM Integration | LangChain Google GenAI (langchain-google-genai) |
| Backend | Flask + Flask-CORS |
| Frontend | Vanilla HTML/CSS/JS - no framework |
| Voice | Web Speech API (browser-native, no external service) |
| Environment | python-dotenv |
| External APIs | Google Generative Language API only |

---

## Agent Graph Topology

```
START
  └── Research Agent
        ├── Finance Agent ──────────┐
        └── Marketing Agent ────────┴── Challenge Agent
                                              ├── Operations Agent ──┐
                                              └── Devil's Advocate ──┴── CEO Agent
                                                                            └── Surprise Agent (if surprise input)
                                                                                  └── END
```

Two fan-outs and two fan-ins. Each agent is a separate LangGraph node with its own LLM instance.

---

## Known Limitations and Failure Handling

1. **Rate limits:** Each swarm run makes 7-8 Gemini API calls. Free tier allows 15 RPM. If rate limited, wait 60 seconds and retry.
2. **Agent failure fallback:** Every agent wraps its LLM call in try/except. If one agent fails, it returns a fallback message and the graph continues - the CEO agent will note the missing input.
3. **Surprise round re-runs full swarm:** The current implementation re-runs all agents when a surprise is injected. A future version would selectively re-run only affected agents.
4. **Sequential fan-out:** LangGraph runs parallel fan-out nodes sequentially on a single thread in the default sync executor. True async parallelism requires async node definitions - not implemented in this version.
5. **Context window:** Very long business problems (over 1,000 words) may cause agent outputs to truncate. Keep problem statements under 500 words for best results.
6. **TTS availability:** Voice narration uses the browser Web Speech API. Quality depends on available system voices and may be unavailable on some browsers or OS configurations.

---

## Declaration of Pre-existing and Reused Components

| Component | Source | Usage |
|-----------|--------|-------|
| LangGraph | Open-source, LangChain Inc. | Agent workflow orchestration |
| LangChain Google GenAI | Open-source, LangChain Inc. | Gemini API integration |
| Flask | Open-source, Pallets Projects | Web server |
| Gemini API | Google | LLM inference for all agents |
| Web Speech API | Browser-native W3C standard | TTS voice narration |
| JetBrains Mono font | Open-source, JetBrains | UI typography |

All agent logic, system prompts, graph topology, state design, frontend UI, and boardroom protocol implementation are original work created by Team Agent Zero for this hackathon.

---

## Project Structure

```text
AgentZero/
├── agents/
│   └── swarm.py          # LangGraph swarm - all 8 agent nodes
├── frontend/
│   └── index.html        # Single-page web app
├── app.py                # Flask server + API routes
├── .env                  # API keys (not committed)
├── README.md             # This file
└── requirements.txt      # Dependencies
```

---

## Quick Demo Script (for judges)

1. Open http://127.0.0.1:5000
2. Enter any business problem in the Problem Statement field
3. Click DEPLOY STRATEGY / CONVENE BOARDROOM
4. Watch agents fire in sequence across the Swarm Analytics view
5. Navigate to Decide to see the full CEO directive and KPIs
6. Go to Surprise - inject an unexpected event
7. Watch the swarm adapt and revise the decision

---

*Built at Agentic Swarm Hackathon - Team Agent Zero*
