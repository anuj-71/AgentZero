"""
Central configuration for AI Boardroom.
"""
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL   = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
FLASK_SECRET   = os.getenv("FLASK_SECRET_KEY", "agentic-swarm-secret-2026")
MAX_DEBATE_CYCLES = 3

# Agent voice profiles - used by the TTS engine
# pitch/rate are hints stored here; actual synthesis happens in voice.py
AGENT_VOICES = {
    "Research":    {"voice_id": 0, "rate": 155, "pitch": "medium",    "color": "#6366f1"},
    "Finance":     {"voice_id": 1, "rate": 145, "pitch": "low",       "color": "#10b981"},
    "Marketing":   {"voice_id": 0, "rate": 170, "pitch": "high",      "color": "#f59e0b"},
    "Operations":  {"voice_id": 1, "rate": 150, "pitch": "medium",    "color": "#3b82f6"},
    "Risk":        {"voice_id": 0, "rate": 140, "pitch": "low",       "color": "#ef4444"},
    "CEO":         {"voice_id": 1, "rate": 135, "pitch": "very_low",  "color": "#8b5cf6"},
}

# Business challenges catalogue
CHALLENGES = [
    {
        "id": "retail_expansion",
        "title": "Retail Chain: International Expansion",
        "brief": (
            "FreshMart, a profitable mid-size grocery retail chain with 120 stores across "
            "the UK, is evaluating expanding into Germany and Poland. The company has £50M "
            "earmarked for international growth. Competitors include Lidl, Aldi and local "
            "discount chains. FreshMart's differentiator is premium-fresh produce and a "
            "loyalty programme with 2M active members. The CEO must decide whether to "
            "enter Germany, Poland, both markets, or invest the £50M domestically instead."
        ),
        "context": {
            "budget": "£50M",
            "current_stores": 120,
            "home_market": "UK",
            "target_markets": ["Germany", "Poland"],
            "differentiator": "Premium-fresh produce + 2M member loyalty programme",
            "competitors": ["Lidl", "Aldi", "Local discount chains"],
        },
        "surprise_options": [
            {
                "id": "supply_disruption",
                "title": "Supply Chain Disruption",
                "description": (
                    "A major fresh-produce supplier covering 40% of FreshMart's European "
                    "supply has announced insolvency. Sourcing alternatives will add £8M "
                    "in Year-1 costs and delay store openings by 6 months."
                ),
            },
            {
                "id": "competitor_entry",
                "title": "US Mega-Retailer Entry",
                "description": (
                    "Whole Foods (Amazon) has announced aggressive UK expansion with 30 new "
                    "stores, directly targeting FreshMart's premium segment. Domestic market "
                    "share is at risk, suggesting the £50M may be better deployed at home."
                ),
            },
        ],
    },
    {
        "id": "fintech_launch",
        "title": "FinTech Startup: B2B Payments Product Launch",
        "brief": (
            "PayBridge is a Series-A FinTech startup with $12M funding. They have built a "
            "B2B cross-border payments API targeting SMEs in Southeast Asia. They must "
            "decide whether to launch first in Singapore, Indonesia or both simultaneously. "
            "Monthly burn rate is $400K. Competitors include Wise Business and Airwallex. "
            "The CEO must choose a go-to-market strategy that maximises 18-month runway."
        ),
        "context": {
            "budget": "$12M",
            "burn_rate": "$400K/month",
            "runway": "30 months at current burn",
            "target_markets": ["Singapore", "Indonesia"],
            "product": "B2B cross-border payments API",
            "competitors": ["Wise Business", "Airwallex"],
        },
        "surprise_options": [
            {
                "id": "regulatory_block",
                "title": "Regulatory Block in Indonesia",
                "description": (
                    "Bank Indonesia has introduced new licensing requirements that will take "
                    "12-18 months to obtain, effectively closing the Indonesian market for "
                    "the near term. The team must reassess the entire go-to-market strategy."
                ),
            },
            {
                "id": "acqui_offer",
                "title": "Acquisition Offer Received",
                "description": (
                    "A Tier-1 bank has offered $45M to acquire PayBridge before launch. "
                    "Founders can accept, reject, or use it as leverage. The board must "
                    "weigh exit vs. independent growth against the competitive landscape."
                ),
            },
        ],
    },
    {
        "id": "saas_pivot",
        "title": "SaaS Company: AI Feature Pivot",
        "brief": (
            "TaskFlow is a project-management SaaS with 15,000 paying SME customers and "
            "$8M ARR. They must decide whether to invest $3M in building proprietary AI "
            "features, licensing an existing AI platform, or acquiring a small AI startup "
            "for $5M. Churn has risen to 8% due to competitors launching AI tools. "
            "The CEO must choose a strategy to reduce churn and grow ARR by 40% in 18 months."
        ),
        "context": {
            "ARR": "$8M",
            "customers": "15,000 SMEs",
            "churn": "8% annually",
            "investment_budget": "$3M-$5M",
            "target": "40% ARR growth in 18 months",
            "options": ["Build proprietary AI", "License AI platform", "Acquire AI startup"],
        },
        "surprise_options": [
            {
                "id": "big_tech_competition",
                "title": "Microsoft Copilot Integration Announced",
                "description": (
                    "Microsoft has announced deep Copilot integration into Teams and "
                    "Planner, directly commoditising TaskFlow's planned AI features. "
                    "The build-vs-buy calculus has fundamentally shifted."
                ),
            },
            {
                "id": "funding_cut",
                "title": "Investor Pulls $2M from Round",
                "description": (
                    "A key investor has withdrawn $2M from the planned investment round, "
                    "reducing available capital to $1M-$3M. The acquisition option is now "
                    "out of reach. Strategy must be revised within the new budget constraint."
                ),
            },
        ],
    },
]
