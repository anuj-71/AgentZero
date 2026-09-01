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

api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment or .env file.")

model_name = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")

llm = ChatGoogleGenerativeAI(
    model=model_name,
    api_key=api_key,
)


def take_last(current: str, new: str) -> str:
    return new


class SwarmState(TypedDict):
    business_problem: str
    research_output: str
    finance_output: str
    marketing_output: str
    challenge_log: str
    ceo_decision: str
    kpis: list[str]
    surprise_input: str
    revised_decision: str
    current_stage: Annotated[str, take_last]
    trace: Annotated[list[str], operator.add]


def _call_llm(system_prompt: str, user_content: str) -> str:
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content},
    ]
    response = llm.invoke(messages)
    content = response.content
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts = []
        for part in content:
            if isinstance(part, dict) and "text" in part:
                parts.append(part["text"])
            elif isinstance(part, str):
                parts.append(part)
        return "".join(parts).strip()
    return str(content).strip()


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
        "Be specific. Output structured findings in 4 bullet points maximum."
    )
    user_input = state["business_problem"]
    output = _call_llm(system_prompt, user_input)
    return {
        "research_output": output,
        "current_stage": "research",
        "trace": ["[RESEARCH] Analysis complete"],
    }


def finance_agent(state: SwarmState) -> dict:
    system_prompt = (
        "You are the Finance Agent. Based on the business problem and research findings provided, "
        "evaluate: estimated costs, revenue potential, break-even assumptions, financial risks. "
        "Give a clear RECOMMEND or DO NOT RECOMMEND with one key financial reason."
    )
    user_input = (
        f"Business Problem:\n{state['business_problem']}\n\n"
        f"Research Findings:\n{state['research_output']}"
    )
    output = _call_llm(system_prompt, user_input)
    return {
        "finance_output": output,
        "current_stage": "finance",
        "trace": ["[FINANCE] Evaluation complete"],
    }


def marketing_agent(state: SwarmState) -> dict:
    system_prompt = (
        "You are the Marketing and Sales Agent. Based on the business problem and research findings, "
        "define: target customer segment, positioning statement, top 2 acquisition channels, "
        "one key marketing risk. Give a clear GO or NO-GO recommendation."
    )
    user_input = (
        f"Business Problem:\n{state['business_problem']}\n\n"
        f"Research Findings:\n{state['research_output']}"
    )
    output = _call_llm(system_prompt, user_input)
    return {
        "marketing_output": output,
        "current_stage": "marketing",
        "trace": ["[MARKETING] Strategy complete"],
    }


def challenge_node(state: SwarmState) -> dict:
    system_prompt = (
        "You are a critical reviewer. Read the Finance and Marketing outputs. "
        "Find the single most important disagreement or conflict between them. "
        "State what Finance says, what Marketing says, and why they conflict. "
        "Then propose the resolution the CEO should consider."
    )
    user_input = (
        f"Finance Evaluation:\n{state['finance_output']}\n\n"
        f"Marketing Strategy:\n{state['marketing_output']}"
    )
    output = _call_llm(system_prompt, user_input)
    return {
        "challenge_log": output,
        "current_stage": "challenge",
        "trace": ["[CHALLENGE] Disagreement identified"],
    }


def ceo_agent(state: SwarmState) -> dict:
    system_prompt = (
        "You are the CEO Agent. You have received inputs from Research, Finance, Marketing, "
        "and a Challenge review. Your output must contain exactly these sections:\n"
        "DECISION: [one clear sentence]\n"
        "EVIDENCE USED: [2-3 points from department agents]\n"
        "REJECTED ALTERNATIVE: [one option and why rejected]\n"
        "KEY RISKS: [2 risks]\n"
        "IMPLEMENTATION: [3 ordered steps]\n"
        "KPIs: [exactly 3 measurable KPIs]"
    )
    user_input = (
        f"Business Problem:\n{state['business_problem']}\n\n"
        f"Research Findings:\n{state['research_output']}\n\n"
        f"Finance Evaluation:\n{state['finance_output']}\n\n"
        f"Marketing Strategy:\n{state['marketing_output']}\n\n"
        f"Challenge Review:\n{state['challenge_log']}"
    )
    output = _call_llm(system_prompt, user_input)
    kpis = _parse_kpis(output)
    return {
        "ceo_decision": output,
        "kpis": kpis,
        "current_stage": "ceo",
        "trace": ["[CEO] Final decision issued"],
    }


def surprise_agent(state: SwarmState) -> dict:
    system_prompt = (
        "You are the CEO Agent handling an unexpected business development. "
        "A surprise event has occurred. Re-evaluate your previous decision given this new information. "
        "Output:\n"
        "WHAT CHANGED: [the new fact]\n"
        "WHAT STAYS THE SAME: [unchanged elements]\n"
        "REVISED DECISION: [updated strategy]\n"
        "UPDATED KPIs: [3 KPIs reflecting the change]"
    )
    user_input = (
        f"Original CEO Decision:\n{state['ceo_decision']}\n\n"
        f"Surprise Event:\n{state['surprise_input']}"
    )
    output = _call_llm(system_prompt, user_input)
    return {
        "revised_decision": output,
        "current_stage": "surprise",
        "trace": ["[SURPRISE] Revised decision issued"],
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
workflow.add_node("ceo_agent", ceo_agent)
workflow.add_node("surprise_agent", surprise_agent)

workflow.add_edge(START, "research_agent")
workflow.add_edge("research_agent", "finance_agent")
workflow.add_edge("research_agent", "marketing_agent")
workflow.add_edge("finance_agent", "challenge_node")
workflow.add_edge("marketing_agent", "challenge_node")
workflow.add_edge("challenge_node", "ceo_agent")
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
