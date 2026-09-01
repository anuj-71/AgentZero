import json
import os
from agents.swarm import run_swarm

TESTCASES = [
    {
        "id": "TC1",
        "title": "TC1: BASELINE - LAUNCH THE SMALL-BUSINESS LOAN",
        "problem": (
            "FinNova Capital has INR 30 crore available for a one-year small-business lending pilot and INR 60 lakh for customer acquisition. "
            "It can initially approve no more than 700 loans. Common costs: Cost of funds 10% per year, Servicing and collections cost 1.5% of principal per year, "
            "Product setup cost INR 18 lakh (deducted from acquisition budget). Segment data: Retail shops avg loan INR 4L, 5% default, 1500 demand, INR 2,000 CAC; "
            "Service SMEs avg loan INR 6L, 3.5% default, 900 demand, INR 3,500 CAC; Small manufacturers avg loan INR 9L, 4.5% default, 450 demand, INR 5,500 CAC. "
            "Constraints: Expected portfolio default <= 5%, Max interest 19%, No segment > 70% of capital, At least INR 3 crore liquid reserve, Max 700 approved loans. "
            "Question: Which segment mix, pricing, approval policy and launch plan creates the strongest risk-adjusted business outcome?"
        ),
        "surprise": ""
    },
    {
        "id": "TC2",
        "title": "TC2: SURPRISE - CREDIT-RISK SPIKE",
        "problem": (
            "FinNova Capital is running a one-year INR 27 crore pilot with 600 planned loans (Retail 45%, Service SMEs 35%, Small manufacturers 20%, 17% interest, 10% cost of funds, 1.5% servicing). "
            "New condition: Retail expected default rises to 8%, Service SME expected default rises to 5%, Small manufacturer expected default rises to 7%. "
            "Risk committee requires expected portfolio default to remain at or below 5.5%. Tighter approval rules reduce eligible demand by 25%. "
            "Pausing creates INR 12 lakh sunk launch costs. All changes within 30 days. "
            "Question: Should FinNova continue, redesign or pause the pilot? Specify revised portfolio, pricing, controls and implementation plan."
        ),
        "surprise": "Retail default rose to 8%, Service SME to 5%, Manufacturer to 7%. Risk committee mandates <= 5.5% portfolio default."
    },
    {
        "id": "TC3",
        "title": "TC3: SURPRISE - MARKETING BUDGET CUT",
        "problem": (
            "FinNova Capital will launch in eight weeks. Customer acquisition budget reduced from INR 60 lakh to INR 36 lakh. "
            "Setup requires INR 18 lakh, leaving INR 18 lakh for marketing. Target: >= 400 qualified applications, >= 160 funded loans. "
            "Channels: Partner accountants (INR 3,000 CPA, 45% conversion), Digital ads (INR 1,800 CPA, 25% conversion), "
            "Trade associations (INR 4,000 CPA, 60% conversion), Existing customer referrals (INR 1,200 CPA, 40% conversion, max 120 apps). "
            "Constraints: Marketing spend <= INR 18 lakh, max 65% in one channel, launch delay <= 2 weeks, transparent pricing and repayment obligations. "
            "Question: How should the reduced budget be allocated? Should target segment, launch timing or funded-loan target be revised?"
        ),
        "surprise": "Marketing budget cut to INR 18 lakh net. Must achieve >= 400 qualified applications and >= 160 funded loans across 4 channels."
    },
    {
        "id": "TC4",
        "title": "TC4: SURPRISE - STRICTER VERIFICATION REQUIREMENTS",
        "problem": (
            "FinNova Capital processes 500 applications/week, approves 35% (175/week), 12-minute onboarding, uses manual verification for 10% (17.5/week), "
            "employs 8 reviewers (each does 4 reviews/day, 5 days/week = 160 reviews/week capacity). "
            "New requirement: Enhanced ownership and bank-statement verification before disbursement. Automated checks clear 60%. Remaining 40% require manual review (70/week). "
            "Options: Hire 4 temporary reviewers at INR 45,000/month each, reduce intake, appointment-based onboarding, delay launch up to 4 weeks, "
            "integrate automated verification service (costs INR 8 lakh, 2 weeks). "
            "Constraints: 3-month budget INR 15 lakh, median approval < 48 hours, complaint rate < 2%, zero disbursement before verification. "
            "Question: What operating model should FinNova implement to satisfy the new verification requirement without unacceptable delays or customer harm?"
        ),
        "surprise": "Mandatory enhanced verification: 40% manual review required before disbursement. 3-month budget INR 15 lakh, approval < 48 hours."
    },
    {
        "id": "TC5",
        "title": "TC5: LIVE TEST - FUNDING-COST AND FRAUD SHOCK",
        "problem": (
            "FinNova Capital approved plan to deploy INR 24 crore across 500 loans (17.5% interest, 4.5% default, 10% cost of funds, 1.5% servicing, 50% retail, 2% suspected fraud). "
            "Live shock: Cost of funds rises to 13%, suspected retail fraud rises to 7%. "
            "Controls: Fraud-screening service (costs INR 1,200/retail app, cuts fraud 60%), reduce retail allocation, increase pricing up to 19%, "
            "introduce manual review, reduce total capital deployment, delay retail launch. "
            "Fixed limits: >= INR 3 crore liquid reserve, expected portfolio default after controls <= 5.5%, max customer interest 19%. "
            "Question: Revise portfolio, controls, pricing and launch decision. Identify which original assumptions are no longer valid."
        ),
        "surprise": "Cost of funds surged to 13%, Retail fraud jumped to 7%. Maintain >= INR 3 crore liquid, default <= 5.5%, interest <= 19%."
    }
]

def main():
    results = []
    for tc in TESTCASES:
        print(f"Running {tc['id']}...")
        res = run_swarm(tc["problem"], tc["surprise"])
        results.append({
            "id": tc["id"],
            "title": tc["title"],
            "problem": tc["problem"],
            "surprise": tc["surprise"],
            "research": res.get("research_output", ""),
            "finance": res.get("finance_output", ""),
            "marketing": res.get("marketing_output", ""),
            "credit_risk": res.get("credit_risk_output", ""),
            "compliance": res.get("compliance_output", ""),
            "challenge": res.get("challenge_log", ""),
            "ceo_decision": res.get("ceo_decision", ""),
            "kpis": res.get("kpis", []),
            "revised_decision": res.get("revised_decision", ""),
            "trace": res.get("trace", [])
        })
        print(f"Finished {tc['id']}.")

    os.makedirs("data", exist_ok=True)
    with open("data/testcases_report.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print("Saved all results to data/testcases_report.json")

if __name__ == "__main__":
    main()
