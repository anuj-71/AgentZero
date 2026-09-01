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
| Conflict Reviewer | Identifies and reconciles material disagreements between departmental recommendations | Finance + Marketing outputs | Specific disagreement, reconciliation, and recommended resolution |

---

## Evidence and Assumptions Policy

- Challenge-specific inputs are taken from the supplied Theme A / FinSwarm test cases.
- Supplied case facts are treated as constraints and are not silently modified.
- Any model-derived estimates, forecasts, thresholds, or operational assumptions are clearly identified as assumptions.
- External services and APIs are used only for the functionality described in this README.
- The swarm does not rely on hardcoded final business decisions; recommendations are generated dynamically from the supplied business problem and agent context.
- During a Surprise Round, changed facts are explicitly identified before the affected decision is reconsidered.

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

### Visual Architecture

```mermaid
graph TD
    START([START]) --> NEXUS[Research Agent<br/>NEXUS<br/>Market Analysis]
    
    NEXUS --> AURA[Finance Agent<br/>AURA<br/>Financial Evaluation]
    NEXUS --> ECHO[Marketing Agent<br/>ECHO<br/>GTM Strategy]
    
    AURA --> CHALLENGE{Challenge Node<br/>Conflict Reviewer<br/>Finance vs Marketing}
    ECHO --> CHALLENGE
    
    CHALLENGE --> VEX[Credit Risk Agent<br/>VEX<br/>Portfolio Stress Test]
    
    VEX --> COG[Compliance Agent<br/>COG<br/>Regulatory Check]
    
    COG --> PRIME[CEO Agent<br/>PRIME<br/>Final Decision]
    
    PRIME --> SURPRISE_CHECK{Surprise Event?}
    
    SURPRISE_CHECK -->|Yes| ADAPTIVE[Adaptive Scenario Agent<br/>Revised Decision]
    SURPRISE_CHECK -->|No| END([END])
    
    ADAPTIVE --> END
    
    style START fill:#e1f5e1
    style END fill:#ffe1e1
    style NEXUS fill:#e3f2fd
    style AURA fill:#fff3e0
    style ECHO fill:#f3e5f5
    style CHALLENGE fill:#fff9c4
    style VEX fill:#ffebee
    style COG fill:#e0f2f1
    style PRIME fill:#fce4ec
    style ADAPTIVE fill:#f1f8e9
    style SURPRISE_CHECK fill:#fff3e0
```

### Execution Flow

```
START
  └── Research Agent (NEXUS)
        ├── Finance & Treasury Agent (AURA) ────────┐
        └── Marketing & Sales Agent (ECHO) ─────────┴── Conflict Reviewer (Challenge Node)
                                                              └── Credit Risk Agent (VEX)
                                                                    └── Compliance Agent (COG)
                                                                          └── CEO Agent (PRIME)
                                                                                └── [Conditional] Adaptive Surprise Agent
                                                                                      └── END
```

### State Management

The swarm uses LangGraph's `StateGraph` with typed state dictionary:

| State Field | Type | Purpose |
|------------|------|---------|
| `business_problem` | str | Input business case |
| `research_output` | str | NEXUS market analysis |
| `finance_output` | str | AURA financial recommendation |
| `marketing_output` | str | ECHO GTM strategy |
| `credit_risk_output` | str | VEX portfolio risk assessment |
| `compliance_output` | str | COG regulatory check |
| `challenge_log` | str | Conflict identification & resolution |
| `ceo_decision` | str | PRIME final directive |
| `kpis` | list[str] | Measurable business KPIs |
| `surprise_input` | str | Unexpected market event |
| `revised_decision` | str | Adaptive CEO response |
| `current_stage` | str | Current execution phase |
| `trace` | list[str] | Audit log of all agent activities |

### Agent Communication Pattern

1. **Fan-out:** Research agent outputs are consumed by Finance and Marketing in parallel
2. **Synchronization:** Challenge node waits for both Finance and Marketing before proceeding
3. **Sequential:** Credit Risk → Compliance → CEO form a linear validation chain
4. **Conditional:** Surprise agent only activates if `surprise_input` is provided
5. **State-based:** All agents read from and write to shared state dictionary

#### Surprise Adaptation Protocol

When a surprise event is provided, the system identifies changed assumptions, re-evaluates affected agents, performs a second challenge/comparison, and generates a revised decision with updated KPIs. The adaptation reuses the existing workflow and does not require a full rebuild.
Structured boardroom execution: Each specialist agent runs as an isolated LangGraph node with its own domain prompt and context injection.

---
### Debate and Termination Control

The boardroom workflow is bounded and terminates after the defined decision stages. Debate/review is not an uncontrolled conversation loop and is capped at a maximum of three review cycles. The CEO node always produces a final decision, including when a non-CEO agent fails.

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
│   └── swarm.py              # LangGraph swarm - 8 identifiable workflow agents/nodes
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

---

## How to Run the Application

### Method 1: Web Interface (Recommended for Judges)

1. **Start the server:**
   ```bash
   python app.py
   ```

2. **Open in browser:**
   ```
   http://127.0.0.1:5000
   ```

3. **Enter business problem:**
   - Paste any test case problem statement (see Test Cases section below)
   - Click "CONVENE BOARDROOM" or "DEPLOY STRATEGY"
   - Watch agents execute in real-time

4. **View results:**
   - Research, Finance, Marketing, Credit Risk, Compliance outputs
   - CEO decision with evidence, risks, and KPIs
   - Full execution trace

5. **Test surprise round:**
   - Enter a surprise event (e.g., "Cost of funds rises to 13%")
   - Click submit to see adaptive decision

---

### Method 2: Command Line (For Quick Testing)

**Basic run (no surprise):**
```bash
python agents/swarm.py "Your business problem here"
```

**With surprise event:**
```bash
python agents/swarm.py "Your business problem" "Your surprise event"
```

**Example:**
```bash
python agents/swarm.py "FinNova Capital has INR 30 crore available for a small-business lending pilot..." ""
```

---

### Method 3: Run All Theme A Test Cases

**Generate complete test case report:**
```bash
python run_all_tc.py
```

This will:
- Execute all 5 Theme A test cases (TC1-TC5)
- Generate full agent outputs for each test case
- Save results to `data/testcases_report.json`
- Takes approximately 5-10 minutes depending on API response time

**View the report:**
```bash
# Start server
python app.py

# Open browser and navigate to:
http://127.0.0.1:5000/api/testcases-report
```
---

*Built at Agentic Swarm Hackathon - Team Agent Zero*
