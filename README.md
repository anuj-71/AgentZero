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
| Business Research Agent (NEXUS) | Market analysis - opportunity, segment demand, competitors, risks | Business problem statement | 4-point research brief forwarded to Finance, Marketing, Compliance |
| Finance and Treasury Agent (AURA) | Cost of funds, liquidity buffers, revenue, break-even, financial margins | Business problem + Research output | RECOMMEND or DO NOT RECOMMEND with key financial rationale |
| Marketing and Sales Agent (ECHO) | Target segment, positioning, acquisition channels, CAC, marketing risk | Business problem + Research output | GO or NO-GO with channel acquisition strategy |
| Compliance and Customer Protection Agent (COG) | Fair customer treatment, compliance guidelines, operational capacity, execution risk | Business problem + all dept outputs | FEASIBLE or NOT FEASIBLE with operational/compliance risk |
| Credit Risk Agent (VEX) | Credit risk, default modeling, stress-tests most dangerous assumption | All department outputs | ASSUMPTION CHALLENGED + WHY IT COULD BE WRONG + WHAT CEO MUST VERIFY |
| CEO Agent (PRIME) | Synthesizes all agent inputs into final executive directive | All department outputs | DECISION + EVIDENCE USED + REJECTED ALTERNATIVE + KEY RISKS + IMPLEMENTATION + 3 KPIs |
| Adaptive Scenario Agent | Re-evaluates corporate decision against a new market or regulatory shock | CEO decision + surprise event | WHAT CHANGED + WHAT STAYS THE SAME + REVISED DECISION + UPDATED KPIs |


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
pip install -r requirements.txt
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
| Frontend | Vanilla HTML/CSS/JS - No framework |
| Voice | ElevenLabs API + Web Speech API fallback |
| Environment | python-dotenv |
| External APIs | Google Generative Language API, ElevenLabs API |

---

## Agent Graph Topology

```
START
  └── Research Agent (NEXUS)
        ├── Finance & Treasury Agent (AURA) ────────┐
        └── Marketing & Sales Agent (ECHO) ─────────┴── Conflict Reviewer (Challenge Node)
                                                              └── Credit Risk Agent (VEX)
                                                                    └── Compliance Agent (COG)
                                                                          └── CEO Agent (PRIME)
                                                                                └── Adaptive Surprise Agent
                                                                                      └── END
```

Structured boardroom execution: Each specialist agent runs as an isolated LangGraph node with its own domain prompt and context injection.

---

## Known Limitations and Failure Handling

1. **Rate limits:** Multi-tier Gemini API key pool fallback with automatic failover across primary and backup keys.
2. **Agent failure fallback:** Every agent wraps its LLM call in try/except. If one agent fails, it returns a fallback message and the graph continues - the CEO agent will note the missing input.
3. **Surprise round:** Adaptive CEO node re-evaluates and pivots corporate strategy upon injected market shocks.
4. **Context window:** Optimized structured prompts with numerical constraint verification prevent truncation.
5. **TTS availability:** ElevenLabs voice synthesis with browser-native Web Speech API fallback.

---

## Declaration of Pre-existing and Reused Components

| Component | Source | Usage |
|-----------|--------|-------|
| LangGraph | Open-source, LangChain Inc. | Agent workflow orchestration |
| LangChain Google GenAI | Open-source, LangChain Inc. | Gemini API integration |
| Flask | Open-source, Pallets Projects | Web server |
| Gemini API | Google | LLM inference for all agents |
| ElevenLabs API | ElevenLabs | Voice synthesis for boardroom agents |
| Web Speech API | Browser-native W3C standard | TTS voice narration fallback |
| jsPDF | Open-source, Parallax | Client-side dynamic PDF report generation |

All agent logic, system prompts, graph topology, state design, frontend UI, and boardroom protocol implementation are original work created by Team Agent Zero for this hackathon.

---

## Project Structure

```text
AgentZero/
├── agents/
│   └── swarm.py              # LangGraph swarm - all 8 agent nodes
├── ai_boardroom/
│   ├── templates/
│   │   └── index.html        # Interactive AI Boardroom UI & PDF Report Generator
│   ├── core/
│   │   └── config.py         # Swarm configurations & presets
│   └── open_app.py           # Quick-launch browser opener
├── frontend/
│   └── index.html            # Terminal UI alternative
├── data/
│   └── testcases_report.json # Theme A comprehensive 5-testcase evaluation data
├── app.py                    # Flask server + API routes (/api/run, /api/tts, /api/testcases-report)
├── run_all_tc.py             # Test harness to execute all 5 Theme A test cases
├── .env.example              # Environment variables template (no keys committed)
├── .gitignore                # Git ignore rules (.env protected)
├── README.md                 # Project documentation
└── requirements.txt          # Python dependencies
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
