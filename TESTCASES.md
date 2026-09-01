# Theme A Test Cases - Quick Reference

## Purpose

This file contains all 5 official Theme A (FinSwarm) test cases for easy copy-paste testing.

**IMPORTANT:** These test cases are NOT hardcoded in the swarm. The agents analyze them dynamically using LLMs. You can modify any test case or create entirely new business problems - the swarm will adapt.

---

## TC1: BASELINE - LAUNCH THE SMALL-BUSINESS LOAN

**Type:** Baseline decision (no surprise)

**Problem Statement:**
```
FinNova Capital has INR 30 crore available for a one-year small-business lending pilot and INR 60 lakh for customer acquisition. It can initially approve no more than 700 loans. Common costs: Cost of funds 10% per year, Servicing and collections cost 1.5% of principal per year, Product setup cost INR 18 lakh (deducted from acquisition budget). Segment data: Retail shops avg loan INR 4L, 5% default, 1500 demand, INR 2,000 CAC; Service SMEs avg loan INR 6L, 3.5% default, 900 demand, INR 3,500 CAC; Small manufacturers avg loan INR 9L, 4.5% default, 450 demand, INR 5,500 CAC. Constraints: Expected portfolio default <= 5%, Max interest 19%, No segment > 70% of capital, At least INR 3 crore liquid reserve, Max 700 approved loans. Question: Which segment mix, pricing, approval policy and launch plan creates the strongest risk-adjusted business outcome?
```

**Surprise Event:** (leave empty)

**Expected Decision Elements:**
- Segment allocation across Retail/Service/Manufacturing
- Specific loan counts for each segment
- Interest rate pricing strategy
- Customer acquisition channel allocation
- Risk mitigation (default rate calculation)
- Liquidity reserve verification
- 3 KPIs with numerical targets

---

## TC2: SURPRISE - CREDIT-RISK SPIKE

**Type:** Surprise adaptation

**Problem Statement:**
```
FinNova Capital is running a one-year INR 27 crore pilot with 600 planned loans (Retail 45%, Service SMEs 35%, Small manufacturers 20%, 17% interest, 10% cost of funds, 1.5% servicing). New condition: Retail expected default rises to 8%, Service SME expected default rises to 5%, Small manufacturer expected default rises to 7%. Risk committee requires expected portfolio default to remain at or below 5.5%. Tighter approval rules reduce eligible demand by 25%. Pausing creates INR 12 lakh sunk launch costs. All changes within 30 days. Question: Should FinNova continue, redesign or pause the pilot? Specify revised portfolio, pricing, controls and implementation plan.
```

**Surprise Event:**
```
Retail default rose to 8%, Service SME to 5%, Manufacturer to 7%. Risk committee mandates <= 5.5% portfolio default.
```

**Expected Adaptation:**
- Weighted average default rate calculation (original vs new)
- Continue/Redesign/Pause decision with justification
- Revised segment allocation if redesigning
- Pricing adjustments (tiered or uniform)
- 30-day implementation timeline
- Updated KPIs reflecting new constraints

---

## TC3: SURPRISE - MARKETING BUDGET CUT

**Type:** Surprise adaptation (budget constraint)

**Problem Statement:**
```
FinNova Capital will launch in eight weeks. Customer acquisition budget reduced from INR 60 lakh to INR 36 lakh. Setup requires INR 18 lakh, leaving INR 18 lakh for marketing. Target: >= 400 qualified applications, >= 160 funded loans. Channels: Partner accountants (INR 3,000 CPA, 45% conversion), Digital ads (INR 1,800 CPA, 25% conversion), Trade associations (INR 4,000 CPA, 60% conversion), Existing customer referrals (INR 1,200 CPA, 40% conversion, max 120 apps). Constraints: Marketing spend <= INR 18 lakh, max 65% in one channel, launch delay <= 2 weeks, transparent pricing and repayment obligations. Question: How should the reduced budget be allocated? Should target segment, launch timing or funded-loan target be revised?
```

**Surprise Event:**
```
Marketing budget cut to INR 18 lakh net. Must achieve >= 400 qualified applications and >= 160 funded loans across 4 channels.
```

**Expected Decision:**
- Channel-by-channel budget allocation
- Application count per channel
- Conversion rate × application count = funded loans
- Total budget ≤ INR 18 lakh verification
- Max 65% single-channel constraint check
- Achievability assessment (meet/revise targets)

---

## TC4: SURPRISE - STRICTER VERIFICATION REQUIREMENTS

**Type:** Surprise adaptation (operational capacity)

**Problem Statement:**
```
FinNova Capital processes 500 applications/week, approves 35% (175/week), 12-minute onboarding, uses manual verification for 10% (17.5/week), employs 8 reviewers (each does 4 reviews/day, 5 days/week = 160 reviews/week capacity). New requirement: Enhanced ownership and bank-statement verification before disbursement. Automated checks clear 60%. Remaining 40% require manual review (70/week). Options: Hire 4 temporary reviewers at INR 45,000/month each, reduce intake, appointment-based onboarding, delay launch up to 4 weeks, integrate automated verification service (costs INR 8 lakh, 2 weeks). Constraints: 3-month budget INR 15 lakh, median approval < 48 hours, complaint rate < 2%, zero disbursement before verification. Question: What operating model should FinNova implement to satisfy the new verification requirement without unacceptable delays or customer harm?
```

**Surprise Event:**
```
Mandatory enhanced verification: 40% manual review required before disbursement. 3-month budget INR 15 lakh, approval < 48 hours.
```

**Expected Decision:**
- Current capacity vs new requirement calculation
- Hire temporary reviewers vs automated service vs hybrid
- Cost analysis (3-month budget constraint)
- Timeline impact (launch delay if needed)
- Approval time verification (< 48 hours)
- Zero pre-verification disbursement enforcement

---

## TC5: LIVE TEST - FUNDING-COST AND FRAUD SHOCK

**Type:** Live test (multiple surprise factors)

**Problem Statement:**
```
FinNova Capital approved plan to deploy INR 24 crore across 500 loans (17.5% interest, 4.5% default, 10% cost of funds, 1.5% servicing, 50% retail, 2% suspected fraud). Live shock: Cost of funds rises to 13%, suspected retail fraud rises to 7%. Controls: Fraud-screening service (costs INR 1,200/retail app, cuts fraud 60%), reduce retail allocation, increase pricing up to 19%, introduce manual review, reduce total capital deployment, delay retail launch. Fixed limits: >= INR 3 crore liquid reserve, expected portfolio default after controls <= 5.5%, max customer interest 19%. Question: Revise portfolio, controls, pricing and launch decision. Identify which original assumptions are no longer valid.
```

**Surprise Event:**
```
Cost of funds surged to 13%, Retail fraud jumped to 7%. Maintain >= INR 3 crore liquid, default <= 5.5%, interest <= 19%.
```

**Expected Decision:**
- Original assumptions explicitly identified as invalid
- Margin calculation: Before vs After (show the loss scenario)
- Fraud control cost-benefit analysis
- Pricing adjustment to restore profitability
- Retail allocation reduction strategy
- Post-controls portfolio default verification
- Liquidity reserve maintenance

---

## How to Use These Test Cases

### Web Interface

1. Start server: `python app.py`
2. Open: http://127.0.0.1:5000
3. Copy-paste Problem Statement into the business problem field
4. Copy-paste Surprise Event (if applicable) into the surprise field
5. Click "CONVENE BOARDROOM"

### Command Line

```bash
# TC1 (no surprise)
python agents/swarm.py "FinNova Capital has INR 30 crore..." ""

# TC2 (with surprise)
python agents/swarm.py "FinNova Capital is running..." "Retail default rose to 8%..."
```

### Batch Run All

```bash
python run_all_tc.py
```

This generates `data/testcases_report.json` with all 5 test case results.

---

## Verification Checklist

For each test case, verify the CEO decision includes:

- [ ] **STRATEGY COMPARISON** - Compares at least 2 alternatives
- [ ] **DECISION** - Clear one-sentence selected strategy
- [ ] **EVIDENCE USED** - Cites agents by name (Finance, Credit Risk, etc.)
- [ ] **REJECTED ALTERNATIVE** - States what was NOT chosen and why
- [ ] **KEY RISKS** - Lists 2-3 risks with numerical thresholds
- [ ] **IMPLEMENTATION** - 3 numbered steps with responsible departments
- [ ] **KPIs** - At least 3 measurable KPIs with numerical targets

For surprise rounds (TC2-TC5), also verify:

- [ ] **WHAT CHANGED** - Identifies new facts/assumptions
- [ ] **WHAT STAYS THE SAME** - States unchanged elements
- [ ] **REVISED DECISION** - Updated strategy reflecting surprise
- [ ] **UPDATED KPIs** - Modified metrics for new situation

---

## Testing Custom Scenarios

The swarm is NOT limited to these 5 test cases. You can test with:

**Modified constraints:**
```
FinNova Capital has INR 50 crore available (instead of 30)...
```

**New surprise events:**
```
Surprise: RBI introduces 15% interest cap (instead of 19%)
```

**Different business problems:**
```
TechLend India wants to launch a student education loan product...
```

The agents will analyze ANY business problem that involves:
- Financial constraints (capital, budget, costs)
- Risk assessment (default rates, fraud)
- Regulatory compliance (interest caps, reserves)
- Market segments and customer acquisition
- Strategic decision-making

---

## Notes on Dynamic Generation

**Important:** The swarm does NOT have these test cases memorized. Each run:

1. ✅ Parses the problem statement dynamically
2. ✅ Extracts numerical constraints from text
3. ✅ Generates agent-specific analysis via LLM calls
4. ✅ Synthesizes results in CEO decision format
5. ✅ Adapts to surprise events in real-time

**Evidence:**
- Modify any number in a test case (change "INR 30 crore" to "INR 25 crore")
- The agents will recalculate and adapt their decisions
- Results reflect the modified constraints, not the original test case

This demonstrates genuine multi-agent collaboration, not pre-programmed responses.
