import os
import re
import sys
import operator
import warnings
from typing import TypedDict, Annotated
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

warnings.filterwarnings("ignore", category=UserWarning, module="langchain_google_genai")

load_dotenv()

model_name = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")


def _get_api_keys() -> list[str]:
    raw_keys = [
        os.getenv("GOOGLE_API_KEY"),
        os.getenv("GEMINI_API_KEY"),
        os.getenv("Bckp1_API"),
        os.getenv("GEMINI_BACKUP_KEY_1"),
        os.getenv("Bckp2_API"),
        os.getenv("GEMINI_BACKUP_KEY_2"),
    ]
    keys: list[str] = []
    seen = set()
    for k in raw_keys:
        if k and k.strip() and k.strip() not in seen:
            seen.add(k.strip())
            keys.append(k.strip())
    return keys


_CURRENT_KEY_INDEX = 0
_all_keys = _get_api_keys()
_primary_key = _all_keys[0] if _all_keys else None

research_llm = ChatGoogleGenerativeAI(model=model_name, api_key=_primary_key)
finance_llm = ChatGoogleGenerativeAI(model=model_name, api_key=_primary_key)
marketing_llm = ChatGoogleGenerativeAI(model=model_name, api_key=_primary_key)
challenge_llm = ChatGoogleGenerativeAI(model=model_name, api_key=_primary_key)
operations_llm = ChatGoogleGenerativeAI(model=model_name, api_key=_primary_key)
devils_llm = ChatGoogleGenerativeAI(model=model_name, api_key=_primary_key)
ceo_llm = ChatGoogleGenerativeAI(model=model_name, api_key=_primary_key)
surprise_llm = ChatGoogleGenerativeAI(model=model_name, api_key=_primary_key)


def take_last(current: str, new: str) -> str:
    return new


class SwarmState(TypedDict):
    business_problem: str
    research_output: str
    finance_output: str
    marketing_output: str
    operations_output: str
    devils_advocate_output: str
    challenge_log: str
    ceo_decision: str
    kpis: list[str]
    surprise_input: str
    revised_decision: str
    current_stage: Annotated[str, take_last]
    trace: Annotated[list[str], operator.add]


def _clean(text: str) -> str:
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    text = re.sub(r"#{1,6}\s*", "", text)
    text = re.sub(r"`{1,3}", "", text)
    return text.strip()


def _call_llm(llm_instance: ChatGoogleGenerativeAI, system_prompt: str, user_content: str, agent_name: str = "Agent") -> str:
    global _CURRENT_KEY_INDEX
    keys = _get_api_keys()
    if not keys:
        return f"[AGENT ERROR] {agent_name} failed: No Gemini API keys found in environment."

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content},
    ]

    last_error = ""
    for attempt in range(len(keys)):
        idx = (_CURRENT_KEY_INDEX + attempt) % len(keys)
        active_key = keys[idx]
        try:
            active_llm = ChatGoogleGenerativeAI(model=model_name, api_key=active_key)
            response = active_llm.invoke(messages)
            _CURRENT_KEY_INDEX = idx
            content = response.content
            if isinstance(content, str):
                raw_text = content.strip()
            elif isinstance(content, list):
                parts = []
                for part in content:
                    if isinstance(part, dict) and "text" in part:
                        parts.append(part["text"])
                    elif isinstance(part, str):
                        parts.append(part)
                raw_text = "".join(parts).strip()
            else:
                raw_text = str(content).strip()
            return _clean(raw_text)
        except Exception as e:
            last_error = str(e)
            continue

    return f"[AGENT ERROR] {agent_name} failed across all {len(keys)} API keys: {last_error}. Proceeding with available data."


def _parse_kpis(ceo_text: str) -> list[str]:
    kpis: list[str] = []
    match = re.search(r"KPIs?:\s*(.*)", ceo_text, re.IGNORECASE | re.DOTALL)
    if match:
        section = match.group(1).strip()
        for line in section.splitlines():
            line = line.strip()
            if not line:
                continue
            if re.match(r"^[A-Z\s]{3,}:", line):
                break
            cleaned = re.sub(r"^(\d+[\.\)]|\*|\-|\•|\[\d+\])\s*", "", line).strip()
            if cleaned:
                kpis.append(cleaned)
    return kpis


def research_agent(state: SwarmState) -> dict:
    system_prompt = (
        "You are the Business Research Agent. Analyse the business problem provided. "
        "Cover: market opportunity, target customers, key competitors, main risks. "
        "Be specific. Output structured findings in 4 bullet points maximum. "
        "End your output with: FINDINGS FORWARDED TO: Finance and Treasury Agent, Marketing and Sales Agent, Compliance and Operations Agent"
    )
    user_input = state["business_problem"]
    output = _call_llm(research_llm, system_prompt, user_input, "Business Research Agent")
    return {
        "research_output": output,
        "current_stage": "research",
        "trace": ["[BUSINESS RESEARCH] Analysis complete - forwarded to Finance, Marketing, Operations"],
    }


def finance_agent(state: SwarmState) -> dict:
    system_prompt = (
        "You are the Finance and Treasury Agent. You have received findings from the Business Research Agent. "
        "Based on the business problem and research findings provided, evaluate: estimated costs, cost of funds, "
        "liquidity buffers, revenue potential, break-even assumptions, and financial margins. "
        "Give a clear RECOMMEND or DO NOT RECOMMEND with one key financial reason."
    )
    user_input = (
        f"Business Problem:\n{state['business_problem']}\n\n"
        f"Research Findings:\n{state['research_output']}"
    )
    output = _call_llm(finance_llm, system_prompt, user_input, "Finance and Treasury Agent")
    return {
        "finance_output": output,
        "current_stage": "finance",
        "trace": ["[SHARE] Research brief ingested by Finance and Treasury", "[FINANCE AND TREASURY] Evaluation complete"],
    }


def marketing_agent(state: SwarmState) -> dict:
    system_prompt = (
        "You are the Marketing and Sales Agent. You have received findings from the Business Research Agent. "
        "Based on the business problem and research findings, define: target customer segment, "
        "positioning statement, top 2 acquisition channels, one key marketing risk. "
        "Give a clear GO or NO-GO recommendation."
    )
    user_input = (
        f"Business Problem:\n{state['business_problem']}\n\n"
        f"Research Findings:\n{state['research_output']}"
    )
    output = _call_llm(marketing_llm, system_prompt, user_input, "Marketing and Sales Agent")
    return {
        "marketing_output": output,
        "current_stage": "marketing",
        "trace": ["[SHARE] Research brief ingested by Marketing and Sales", "[MARKETING AND SALES] Strategy complete"],
    }


def challenge_node(state: SwarmState) -> dict:
    system_prompt = (
        "You are the Inter-Department Conflict Reviewer. Finance Agent recommends: [their output]. "
        "Marketing Agent recommends: [their output]. Find where these two departments conflict (e.g. growth vs cost/risk). "
        "State what Finance says, what Marketing says, and why they conflict. "
        "Then propose the resolution the CEO should consider."
    )
    user_input = (
        f"Finance and Treasury Agent recommends:\n{state['finance_output']}\n\n"
        f"Marketing and Sales Agent recommends:\n{state['marketing_output']}"
    )
    output = _call_llm(challenge_llm, system_prompt, user_input, "Conflict Reviewer")
    return {
        "challenge_log": output,
        "current_stage": "challenge",
        "trace": ["[SHARE] Cross-department briefs routed to Conflict Review Node", "[CONFLICT REVIEW] Finance vs Marketing conflict identified"],
    }


def operations_agent(state: SwarmState) -> dict:
    system_prompt = (
        "You are the Compliance and Customer Protection Agent (with Operations responsibility). You have received outputs from Research, Finance, and Marketing Agents. "
        "Evaluate: operational capacity, compliance and regulatory considerations, fair customer treatment, execution bottlenecks, resource requirements. "
        "Give a FEASIBLE or NOT FEASIBLE verdict with the single biggest operational or compliance risk."
    )
    user_input = (
        f"Business Problem:\n{state['business_problem']}\n\n"
        f"Research Findings:\n{state['research_output']}\n\n"
        f"Finance Evaluation:\n{state['finance_output']}\n\n"
        f"Marketing Strategy:\n{state['marketing_output']}"
    )
    output = _call_llm(operations_llm, system_prompt, user_input, "Compliance and Operations Agent")
    return {
        "operations_output": output,
        "current_stage": "operations",
        "trace": ["[SHARE] Department dossiers routed to Compliance and Operations", "[COMPLIANCE AND OPERATIONS] Feasibility assessed"],
    }


def devils_advocate(state: SwarmState) -> dict:
    system_prompt = (
        "You are the Credit Risk Agent (and Devil's Advocate). You have received outputs from Research, Finance, Marketing, AND Compliance/Operations Agents. "
        "Your role is to rigorously evaluate credit risk, default exposure, and challenge the single most dangerous assumption being made across all departments. Output exactly: "
        "ASSUMPTION CHALLENGED: [state it] WHY IT COULD BE WRONG: [credit risk or failure scenario] "
        "WHAT CEO MUST VERIFY: [one specific check or risk control]"
    )
    user_input = (
        f"Business Problem:\n{state['business_problem']}\n\n"
        f"Research Findings:\n{state['research_output']}\n\n"
        f"Finance Evaluation:\n{state['finance_output']}\n\n"
        f"Marketing Strategy:\n{state['marketing_output']}\n\n"
        f"Compliance & Operations Assessment:\n{state['operations_output']}"
    )
    output = _call_llm(devils_llm, system_prompt, user_input, "Credit Risk Agent")
    return {
        "devils_advocate_output": output,
        "current_stage": "devils_advocate",
        "trace": ["[SHARE] Operations and financial models routed to Credit Risk Agent", "[CREDIT RISK] Core assumption and default exposure challenged"],
    }


def ceo_agent(state: SwarmState) -> dict:
    system_prompt = (
        "You are the CEO Agent. You are making the final executive decision for the company. "
        "You have received inputs from: Business Research, Finance and Treasury, Marketing and Sales, Compliance/Operations, "
        "Conflict Reviewer, and Credit Risk Agents.\n\n"
        "First, compare at least two viable strategies in a STRATEGY COMPARISON section.\n"
        "Then synthesize all inputs and output your decision in this EXACT format:\n\n"
        "STRATEGY COMPARISON: [compare Strategy A vs Strategy B with key trade-offs]\n\n"
        "DECISION: [one clear sentence stating the chosen strategy]\n\n"
        "EVIDENCE USED: [explain which department agent outputs influenced this decision, citing agents by name]\n\n"
        "REJECTED ALTERNATIVE: [state the alternative strategy considered and the specific reason it was rejected]\n\n"
        "KEY RISKS: [state 2 critical risks and the trade-offs accepted]\n\n"
        "IMPLEMENTATION: [numbered list of 3 concrete next steps with responsible department functions, e.g. Step 1 (Compliance/Operations): ..., Step 2 (Marketing): ..., Step 3 (Finance): ...]\n\n"
        "KPIs: [numbered list of at least 3 measurable business KPIs with numerical targets]"
    )
    user_input = (
        f"Business Problem:\n{state['business_problem']}\n\n"
        f"Research Findings:\n{state['research_output']}\n\n"
        f"Finance Evaluation:\n{state['finance_output']}\n\n"
        f"Marketing Strategy:\n{state['marketing_output']}\n\n"
        f"Compliance & Operations Assessment:\n{state['operations_output']}\n\n"
        f"Credit Risk Challenge:\n{state['devils_advocate_output']}\n\n"
        f"Conflict Review:\n{state['challenge_log']}"
    )
    output = _call_llm(ceo_llm, system_prompt, user_input, "CEO Agent")
    kpis = _parse_kpis(output)
    return {
        "ceo_decision": output,
        "kpis": kpis,
        "current_stage": "ceo",
        "trace": ["[COMPARE] Executive strategy trade-offs analyzed", "[CEO DECISION] Final executive directive issued"],
    }


def surprise_agent(state: SwarmState) -> dict:
    system_prompt = (
        "A surprise business event has occurred that impacts the company. "
        "You are the Adaptive CEO Agent. Read the original CEO decision and the surprise event. "
        "Re-evaluate the strategy against this new information. "
        "Output your revised decision in this EXACT format:\n\n"
        "WHAT CHANGED: [which assumptions or facts are no longer valid]\n\n"
        "WHAT STAYS THE SAME: [which parts of the original plan hold]\n\n"
        "REVISED DECISION: [the updated decision reflecting the surprise]\n\n"
        "UPDATED KPIs: [3 updated measurable KPIs reflecting the new situation]"
    )
    user_input = (
        f"Original CEO Decision:\n{state['ceo_decision']}\n\n"
        f"Surprise Event:\n{state['surprise_input']}"
    )
    output = _call_llm(surprise_llm, system_prompt, user_input, "Adaptive CEO Agent")
    return {
        "revised_decision": output,
        "current_stage": "surprise",
        "trace": ["[SURPRISE ADAPTATION] Revised strategy issued"],
    }


def _route_after_ceo(state: SwarmState) -> str:
    surprise = state.get("surprise_input", "")
    if surprise and surprise.strip():
        return "surprise_agent"
    return END


workflow = StateGraph(SwarmState)

workflow.add_node("research_agent", research_agent)
workflow.add_node("finance_agent", finance_agent)
workflow.add_node("marketing_agent", marketing_agent)
workflow.add_node("challenge_node", challenge_node)
workflow.add_node("operations_agent", operations_agent)
workflow.add_node("devils_advocate", devils_advocate)
workflow.add_node("ceo_agent", ceo_agent)
workflow.add_node("surprise_agent", surprise_agent)

workflow.add_edge(START, "research_agent")
workflow.add_edge("research_agent", "finance_agent")
workflow.add_edge("research_agent", "marketing_agent")
workflow.add_edge("finance_agent", "challenge_node")
workflow.add_edge("marketing_agent", "challenge_node")
workflow.add_edge("challenge_node", "operations_agent")
workflow.add_edge("operations_agent", "devils_advocate")
workflow.add_edge("devils_advocate", "ceo_agent")
workflow.add_conditional_edges(
    "ceo_agent",
    _route_after_ceo,
    {"surprise_agent": "surprise_agent", END: END},
)
workflow.add_edge("surprise_agent", END)

graph = workflow.compile()


def run_swarm(business_problem: str, surprise: str = "") -> dict:
    initial_state: SwarmState = {
        "business_problem": business_problem,
        "research_output": "",
        "finance_output": "",
        "marketing_output": "",
        "operations_output": "",
        "devils_advocate_output": "",
        "challenge_log": "",
        "ceo_decision": "",
        "kpis": [],
        "surprise_input": surprise,
        "revised_decision": "",
        "current_stage": "init",
        "trace": [],
    }
    return graph.invoke(initial_state)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python agents/swarm.py \"<business_problem>\" [\"<surprise_input>\"]")
        sys.exit(1)

    problem_arg = sys.argv[1]
    surprise_arg = sys.argv[2] if len(sys.argv) > 2 else ""

    final_state = run_swarm(problem_arg, surprise_arg)

    print("\n--- TRACE ---")
    for entry in final_state.get("trace", []):
        print(entry)

    print("\n--- CEO DECISION ---")
    print(final_state.get("ceo_decision", ""))

    if final_state.get("revised_decision"):
        print("\n--- REVISED DECISION (SURPRISE) ---")
        print(final_state.get("revised_decision", ""))
